import asyncio
import time
from collections import defaultdict
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import TypeVar, cast

_CoroutineFunction = TypeVar(
    "_CoroutineFunction", bound=Callable[..., Coroutine[None, None, None]]
)


def debounce(wait: float) -> Callable[[_CoroutineFunction], _CoroutineFunction]:
    def debouncer(coroutinefunction: _CoroutineFunction) -> _CoroutineFunction:
        last_bounce = 0

        @wraps(coroutinefunction)
        async def debounced(*args: object, **kwargs: object) -> None:
            nonlocal last_bounce
            last_bounce += 1
            current_bounce = last_bounce
            await asyncio.sleep(wait)

            if current_bounce == last_bounce:
                await coroutinefunction(*args, **kwargs)

        return cast(_CoroutineFunction, debounced)

    return debouncer


def debouncemethod(wait: float) -> Callable[[_CoroutineFunction], _CoroutineFunction]:
    def debouncer(coroutinefunction: _CoroutineFunction) -> _CoroutineFunction:
        last_bounce_for_object: defaultdict[object, int] = defaultdict(lambda: 0)

        @wraps(coroutinefunction)
        async def debounced(self: object, *args: object, **kwargs: object) -> None:
            last_bounce_for_object[self] += 1
            current_bounce = last_bounce_for_object[self]
            await asyncio.sleep(wait)

            if current_bounce == last_bounce_for_object[self]:
                await coroutinefunction(self, *args, **kwargs)

        return cast(_CoroutineFunction, debounced)

    return debouncer


def throttle(wait: float) -> Callable[[_CoroutineFunction], _CoroutineFunction]:
    def throttler(coroutinefunction: _CoroutineFunction) -> _CoroutineFunction:
        last_call_time = 0.0

        @wraps(coroutinefunction)
        async def throttled(*args: object, **kwargs: object) -> None:
            nonlocal last_call_time
            current_call_time = time.monotonic()

            if current_call_time > last_call_time + wait:
                last_call_time = current_call_time
                await coroutinefunction(*args, **kwargs)

        return cast(_CoroutineFunction, throttled)

    return throttler


def throttlemethod(wait: float) -> Callable[[_CoroutineFunction], _CoroutineFunction]:
    def throttler(coroutinefunction: _CoroutineFunction) -> _CoroutineFunction:
        last_call_time_for_object: defaultdict[object, float] = defaultdict(lambda: 0.0)

        @wraps(coroutinefunction)
        async def throttled(self: object, *args: object, **kwargs: object) -> None:
            current_call_time = time.monotonic()

            if current_call_time > last_call_time_for_object[self] + wait:
                last_call_time_for_object[self] = current_call_time
                await coroutinefunction(self, *args, **kwargs)

        return cast(_CoroutineFunction, throttled)

    return throttler


def unique_name(obj: object, parent_name: str = "", type_name: str = "") -> str:
    if not type_name:
        type_name = type(obj).__name__.lower()

    return f"{parent_name}.{type_name}_{id(obj)}"
