import asyncio
import functools
import logging
import time
from typing import Any, Callable, Dict, Optional

from .client import LLMOutput, NeoApiClient, NeoApiClientSync

logger = logging.getLogger(__name__)


def track_llm_output(
    client: Any,
    project: Optional[str] = "default_project",
    group: Optional[str] = "default_group",
    analysis_slug: Optional[str] = None,
    need_analysis_response: bool = False,
    format_json_output: bool = False,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable:
    """
    Decorator to automatically track LLM outputs.

    Args:
        client (NeoApiClient or NeoApiClientSync): The NeoApiClient instance.
        project (Optional[str]): Project name.
        group (Optional[str]): Group name.
        analysis_slug (Optional[str]): Analysis slug.
        need_analysis_response (bool): Whether an analysis response is needed.
        format_json_output (bool): Whether to format the output as JSON.
        metadata (Optional[Dict[str, Any]]): Additional metadata to include in the output.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Error in function '{func.__name__}': {e}")
                    raise

                llm_output = LLMOutput(
                    text=str(result),
                    timestamp=time.time(),
                    project=project,
                    group=group,
                    analysis_slug=analysis_slug,
                    need_analysis_response=need_analysis_response,
                    format_json_output=format_json_output,
                    metadata=metadata,
                )

                if isinstance(client, NeoApiClient):
                    try:
                        await client.track(llm_output)
                    except Exception as e:
                        logger.exception(f"Failed to track LLM output: {e}")
                elif isinstance(client, NeoApiClientSync):
                    try:
                        client.track(llm_output)
                    except Exception as e:
                        logger.exception(f"Failed to track LLM output: {e}")
                else:
                    logger.error("Unsupported client type provided to decorator.")

                return result

            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Error in function '{func.__name__}': {e}")
                    raise

                llm_output = LLMOutput(
                    text=str(result),
                    timestamp=time.time(),
                    project=project,
                    group=group,
                    analysis_slug=analysis_slug,
                    need_analysis_response=need_analysis_response,
                    format_json_output=format_json_output,
                    metadata=metadata,
                )

                if isinstance(client, NeoApiClientSync):
                    try:
                        client.track(llm_output)
                    except Exception as e:
                        logger.exception(f"Failed to track LLM output: {e}")
                else:
                    logger.error(
                        "For synchronous functions, please provide a NeoApiClientSync instance."
                    )

                return result

            return sync_wrapper

    return decorator
