from typing import Any


def task_response(
    status: str,
    message: str = "",
    error: str | None = None,
    **data,
) -> dict[str, Any]:
    """Helper function to standardize task responses.

    Args:
        status: Status of the task (e.g. 'success', 'error', 'pending').
        message: Description or details about the task result.
        error: Error message if task failed.
        **data: Additional data to include in response.

    Returns:
        Dict containing standardized response with status, message and data.
    """
    response = {"status": status, "message": message}
    if error:
        response["error"] = error
    if data:
        response["data"] = data
    return response


def default_task_params(name: str, **kwargs) -> dict[str, Any]:
    """
    Get common Celery task parameters for tasks.

    Args:
        name: Name of the task.
        **kwargs: Additional task parameters to override defaults.

    Returns:
        Dict of common task parameters with standard retry settings.
    """
    base_params = {
        "bind": True,
        "name": name,
        "max_retries": 5,
        "default_retry_delay": 120,
        "autoretry_for": (Exception,),
        "retry_backoff": True,
        "retry_backoff_max": 900,
        "retry_jitter": True,
    }
    return base_params | kwargs
