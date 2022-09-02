import asyncio
import functools
from random import uniform
from typing import Any, Dict, Optional, Sequence, Union


def prepare_params(**params: Dict[str, Any]) -> Dict[str, Any]:
    cleared_params = dict()
    for key, value in params.items():
        if value == None:
            continue
        elif isinstance(value, bool):
            cleared_params[key] = int(value)
        else:
            cleared_params[key] = value
    return cleared_params


def prepare_json(json: Dict[str, Any]) -> Dict[str, Any]:
    cleared_json = dict()
    for key, value in json.items():
        if value == None:
            continue
        elif isinstance(value, dict):
            nested_cleared_json = prepare_json(value)
            if len(nested_cleared_json) > 0:
                cleared_json[key] = nested_cleared_json
        else:
            cleared_json[key] = value
    return cleared_json


def retry_backoff(
    exceptions: Union[Exception, Sequence[Exception]],
    base_value: int = 1,
    max_time: Optional[int] = None,
    max_attempts: Optional[int] = None,
    jitter: bool = True,
):
    def decorator(callback):
        @functools.wraps(callback)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                attempt += 1

                if max_attempts != None and attempt > max_attempts:
                    attempt = max_attempts

                try:
                    ret = await callback(*args, **kwargs)
                except exceptions as err:
                    print(f"Retry for {type(err).__name__}")

                    seconds = base_value * 2**attempt

                    if max_time != None and seconds > max_time:
                        seconds = max_time

                    if jitter:
                        half_seconds = seconds / 2
                        seconds = int(half_seconds + round(uniform(0, half_seconds), 1))

                    await asyncio.sleep(seconds)
                else:
                    return ret

        return wrapper

    return decorator
