import asyncio
import json
import logging
import threading
import time
from typing import Any, Dict, List, Optional

import aiohttp
import backoff
import requests
from pydantic import BaseModel

from .config import Config
from .exceptions import NeoApiError

logger = logging.getLogger(__name__)


class LLMOutput(BaseModel):
    """
    Represents the output from a Language Model (LLM).

    Attributes:
        text (str): The generated text.
        timestamp (float): The timestamp of the output.
        metadata (Optional[Dict[str, Any]]): Additional metadata.
        project (Optional[str]): Associated project name.
        group (Optional[str]): Associated group name.
        analysis_slug (Optional[str]): Slug for analysis purposes.
        need_analysis_response (bool): Flag indicating if an analysis response is needed.
        format_json_output (bool): Flag to control JSON output formatting.
    """

    text: str
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None
    project: Optional[str] = None
    group: Optional[str] = None
    analysis_slug: Optional[str] = None
    need_analysis_response: bool = False
    format_json_output: bool = False


class NeoApiClient:
    """
    Asynchronous Client for interacting with the Neo API to send LLM outputs.

    Manages batching of LLM outputs and sends them to the Neo API endpoints
    either periodically or when the batch size is reached.
    Additionally, dynamically adjusts batch_size and flush_interval based on current load.
    """

    def __init__(
        self,
        api_key: str,
        initial_batch_size: int = 10,
        initial_flush_interval: float = 5.0,
        max_batch_size: int = 100,
        min_batch_size: int = 5,
        max_flush_interval: float = 10.0,
        min_flush_interval: float = 1.0,
        max_retries: int = 3,
        api_url: Optional[str] = None,
        check_frequency: int = 1,
        adjustment_interval: float = 2.0,
    ):
        if not api_key:
            raise ValueError("API key must be provided.")
        self.api_key = api_key
        self.batch_size = initial_batch_size
        self.flush_interval = initial_flush_interval
        self.max_batch_size = max_batch_size
        self.min_batch_size = min_batch_size
        self.max_flush_interval = max_flush_interval
        self.min_flush_interval = min_flush_interval
        self.max_retries = max_retries

        self.api_url = (api_url or Config.API_URL).rstrip("/")
        self.check_frequency = check_frequency

        self.queue: List[LLMOutput] = []
        self._lock = asyncio.Lock()
        self._flush_task: Optional[asyncio.Task] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self._running = False
        self._semaphore = asyncio.Semaphore(100)

        # Parameters for dynamic adjustment
        self.adjustment_interval = adjustment_interval
        self._adjustment_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """
        Starts the NeoApiClient by initializing the HTTP session and starting
        the periodic flush and adjustment tasks.
        """
        if not self._running:
            logger.debug("Starting NeoApiClient.")
            self.session = aiohttp.ClientSession()
            self._flush_task = asyncio.create_task(self._periodic_flush())
            self._adjustment_task = asyncio.create_task(self._dynamic_adjustment())
            self._running = True
            logger.info("NeoApiClient started.")

    async def stop(self) -> None:
        """
        Stops the NeoApiClient by cancelling the periodic flush and adjustment tasks,
        flushing remaining items, and closing the HTTP session.
        """
        if self._running:
            logger.debug("Stopping NeoApiClient.")
            if self._flush_task:
                self._flush_task.cancel()
                try:
                    await self._flush_task
                except asyncio.CancelledError:
                    logger.debug("Periodic flush task cancelled.")
            if self._adjustment_task:
                self._adjustment_task.cancel()
                try:
                    await self._adjustment_task
                except asyncio.CancelledError:
                    logger.debug("Dynamic adjustment task cancelled.")
            await self.flush()
            if self.session:
                await self.session.close()
                logger.debug("Closed aiohttp ClientSession.")
            self._running = False
            logger.info("NeoApiClient stopped.")

    async def track(self, llm_output: LLMOutput) -> None:
        """
        Tracks an LLMOutput by adding it to the queue and sending the batch if
        the batch size is reached.

        Args:
            llm_output (LLMOutput): The LLMOutput item to track.
        """
        logger.debug(f"Tracking LLM output: {llm_output}")
        async with self._lock:
            self.queue.append(llm_output)
            logger.debug(f"Queue size after append: {len(self.queue)}")
            if len(self.queue) >= self.batch_size:
                logger.debug("Batch size reached, preparing to flush.")
                batch = self.queue.copy()
                self.queue.clear()
                await self._send_batch(batch)

    async def flush(self) -> None:
        """
        Flushes the current queue by sending all queued LLMOutput items.
        """
        logger.debug("Attempting to flush the queue.")
        async with self._lock:
            if not self.queue:
                logger.debug("Queue is empty, nothing to flush.")
                return
            batch = self.queue.copy()
            self.queue.clear()
            logger.debug(f"Flushing {len(batch)} items.")
        await self._send_batch(batch)

    async def _periodic_flush(self) -> None:
        """
        Periodically flushes the queue based on the flush interval.
        """
        logger.debug("Starting periodic flush task.")
        try:
            while True:
                await asyncio.sleep(self.flush_interval)
                logger.debug("Periodic flush triggered.")
                await self.flush()
        except asyncio.CancelledError:
            logger.debug("Periodic flush task cancelled.")

    async def _send_batch(self, batch: List[LLMOutput]) -> None:
        """
        Sends a batch of LLMOutput items to the appropriate Neo API endpoints.

        Args:
            batch (List[LLMOutput]): The batch of LLMOutput items to send.
        """
        if not self.session:
            raise RuntimeError("Client session is not initialized.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        logger.info(f"Starting batch of {len(batch)} LLM outputs to {self.api_url}")

        tasks = []
        for index, item in enumerate(batch):
            if index % self.check_frequency == 0:
                payload = item.model_dump()
                endpoint = "analyze" if item.need_analysis_response else "lib"
                url = f"{self.api_url}/{endpoint}"

                logger.debug(
                    f"Preparing to send item to {url} with project: {payload.get('project')}, "
                    f"group: {payload.get('group')}, analysis_slug: {payload.get('analysis_slug')}."
                )

                task = asyncio.create_task(self._post_item(url, payload, headers, item))
                tasks.append(task)

        if tasks:
            try:
                await self._semaphore.acquire()
                await asyncio.gather(*tasks)
            except Exception as e:
                logger.exception(f"Exception while sending batch: {e}")
                async with self._lock:
                    self.queue.extend(batch)
                raise
            finally:
                self._semaphore.release()
        else:
            logger.debug("No items matched the check frequency for sending.")

    async def _post_item(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        item: LLMOutput,
    ) -> None:
        if not self.session:
            raise RuntimeError("Client session is not initialized")

        session = self.session

        @backoff.on_exception(
            backoff.expo,
            (aiohttp.ClientError, asyncio.TimeoutError),
            max_tries=self.max_retries,
            on_backoff=lambda details: logger.warning(
                f"Retrying send: Attempt {details['tries']} after {details['wait']} seconds."
            ),
        )
        async def send_request() -> None:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 204 and not item.need_analysis_response:
                    text = await response.text()
                    raise NeoApiError(f"Error {response.status}: {text}")
                elif item.need_analysis_response:
                    try:
                        analysis_response = await response.json()
                        if item.format_json_output:
                            formatted_response = json.dumps(analysis_response, indent=4)
                            logger.info(f"Analysis Response:\n{formatted_response}")
                        else:
                            logger.info(f"Analysis Response: {analysis_response}")
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON from analysis response.")
                else:
                    logger.info("Successfully sent item.")

        await send_request()

    async def _dynamic_adjustment(self) -> None:
        """
        Dynamically adjusts the batch_size and flush_interval based on current load.
        """
        logger.debug("Starting dynamic adjustment task.")
        try:
            while True:
                await asyncio.sleep(self.adjustment_interval)
                async with self._lock:
                    queue_length = len(self.queue)
                logger.debug(
                    f"Dynamic Adjustment: Current queue length: {queue_length}"
                )

                if (
                    queue_length > self.batch_size * 1.5
                    and self.batch_size < self.max_batch_size
                ):
                    self.batch_size += 5
                    logger.debug(f"Increasing batch_size to {self.batch_size}")
                elif (
                    queue_length < self.batch_size * 0.5
                    and self.batch_size > self.min_batch_size
                ):
                    self.batch_size -= 5
                    logger.debug(f"Decreasing batch_size to {self.batch_size}")

                if (
                    queue_length > self.batch_size * 2
                    and self.flush_interval > self.min_flush_interval
                ):
                    self.flush_interval = max(
                        self.flush_interval - 0.5, self.min_flush_interval
                    )
                    logger.debug(
                        f"Decreasing flush_interval to {self.flush_interval} seconds"
                    )
                elif (
                    queue_length < self.batch_size
                    and self.flush_interval < self.max_flush_interval
                ):
                    self.flush_interval = min(
                        self.flush_interval + 0.5, self.max_flush_interval
                    )
                    logger.debug(
                        f"Increasing flush_interval to {self.flush_interval} seconds"
                    )
        except asyncio.CancelledError:
            logger.debug("Dynamic adjustment task cancelled.")


class NeoApiClientSync:
    """
    Synchronous Client for interacting with the Neo API to send LLM outputs.

    Manages batching of LLM outputs and sends them to the Neo API endpoints
    either periodically or when the batch size is reached.
    """

    def __init__(
        self,
        api_key: str,
        batch_size: int = 10,
        flush_interval: float = 5.0,
        max_retries: int = 3,
        api_url: Optional[str] = None,
        check_frequency: int = 1,
    ):
        if not api_key:
            raise ValueError("API key must be provided.")
        self.api_key = api_key
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.max_retries = max_retries

        self.api_url = (api_url or Config.API_URL).rstrip("/")
        self.check_frequency = check_frequency

        self.queue: List[LLMOutput] = []
        self._lock = threading.Lock()
        self._flush_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )
        self._semaphore = threading.Semaphore(100)

    def start(self) -> None:
        """
        Starts the NeoApiClientSync by initiating the background flush thread.
        """
        if self._flush_thread is None or not self._flush_thread.is_alive():
            logger.debug("Starting NeoApiClientSync.")
            self._flush_thread = threading.Thread(
                target=self._periodic_flush, daemon=True
            )
            self._flush_thread.start()
            logger.info("NeoApiClientSync started.")

    def stop(self) -> None:
        """
        Stops the NeoApiClientSync by signaling the flush thread to stop,
        flushing remaining items, and closing the HTTP session.
        """
        logger.debug("Stopping NeoApiClientSync.")
        self._stop_event.set()
        if self._flush_thread:
            self._flush_thread.join()
            logger.debug("Flush thread terminated.")
        self.flush()
        self.session.close()
        logger.debug("Closed requests Session.")
        logger.info("NeoApiClientSync stopped.")

    def track(self, llm_output: LLMOutput) -> None:
        """
        Tracks an LLMOutput by adding it to the queue and sending the batch if
        the batch size is reached.

        Args:
            llm_output (LLMOutput): The LLMOutput item to track.
        """
        logger.debug(f"Tracking LLM output: {llm_output}")
        with self._lock:
            self.queue.append(llm_output)
            logger.debug(f"Queue size after append: {len(self.queue)}")
            if len(self.queue) >= self.batch_size:
                logger.debug("Batch size reached, preparing to flush.")
                batch = self.queue.copy()
                self.queue.clear()
                self._send_batch(batch)

    def flush(self) -> None:
        """
        Flushes the current queue by sending all queued LLMOutput items.
        """
        logger.debug("Attempting to flush the queue.")
        with self._lock:
            if not self.queue:
                logger.debug("Queue is empty, nothing to flush.")
                return
            batch = self.queue.copy()
            self.queue.clear()
            logger.debug(f"Flushing {len(batch)} items.")
        self._send_batch(batch)

    def _periodic_flush(self) -> None:
        """
        Periodically flushes the queue based on the flush interval.
        """
        logger.debug("Starting periodic flush thread.")
        while not self._stop_event.is_set():
            time.sleep(self.flush_interval)
            logger.debug("Periodic flush triggered.")
            self.flush()
        logger.debug("Exiting periodic flush thread.")

    def _send_batch(self, batch: List[LLMOutput]) -> None:
        """
        Sends a batch of LLMOutput items to the appropriate Neo API endpoints.

        Args:
            batch (List[LLMOutput]): The batch of LLMOutput items to send.
        """
        if not self.session:
            raise RuntimeError(
                "Client session is not initialized. Call start() before sending requests."
            )

        headers = self.session.headers

        logger.info(f"Sending batch of {len(batch)} LLM outputs to {self.api_url}.")

        threads = []
        for index, item in enumerate(batch):
            if index % self.check_frequency == 0:
                payload = item.model_dump()
                endpoint = "analyze" if item.need_analysis_response else "lib"
                url = f"{self.api_url}/{endpoint}"

                logger.debug(
                    f"Preparing to send item to {url} with project: {payload.get('project')}, "
                    f"group: {payload.get('group')}, analysis_slug: {payload.get('analysis_slug')}."
                )

                thread = threading.Thread(
                    target=self._post_item, args=(url, payload, headers, item)
                )
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

    def _post_item(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        item: LLMOutput,
    ) -> None:
        if not self.session:
            raise RuntimeError("Client session is not initialized")

        session = self.session

        @backoff.on_exception(
            backoff.expo,
            (requests.RequestException, requests.Timeout),
            max_tries=self.max_retries,
            on_backoff=lambda details: logger.warning(
                f"Retrying send: Attempt {details['tries']} after {details['wait']} seconds."
            ),
        )
        def send_request() -> None:
            response = session.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code != 204 and not item.need_analysis_response:
                raise NeoApiError(f"Error {response.status_code}: {response.text}")
            elif item.need_analysis_response:
                try:
                    analysis_response = response.json()
                    if item.format_json_output:
                        formatted_response = json.dumps(analysis_response, indent=4)
                        logger.info(f"Analysis Response:\n{formatted_response}")
                    else:
                        logger.info(f"Analysis Response: {analysis_response}")
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON from analysis response.")
            else:
                logger.info("Successfully sent item.")

        try:
            send_request()
        except Exception as e:
            logger.exception(f"Failed to send item: {e}")

            with self._lock:
                self.queue.append(item)
