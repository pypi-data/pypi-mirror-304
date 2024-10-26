import asyncio
import contextlib
import threading
from collections.abc import Awaitable, Callable, Coroutine
from concurrent.futures import Future


class Asyncio:
    def __init__(self, on_start: Callable[[], Coroutine[None, None, None]]):
        self._on_start = on_start
        self._started = threading.Event()
        self._stopped = asyncio.Event()
        self._thread = threading.Thread(target=asyncio.run, args=(self._main(),))

    def start(self) -> None:
        self._thread.start()
        self._started.wait()

    async def _main(self) -> None:
        self._asyncio_loop = asyncio.get_running_loop()
        self._started.set()

        on_start = asyncio.create_task(self._on_start())
        stopped = asyncio.create_task(self._stopped.wait())
        tasks = (on_start, stopped)

        for task in asyncio.as_completed(tasks):
            with contextlib.suppress(asyncio.CancelledError):
                await task

            if stopped.done() and not on_start.done():
                on_start.cancel()

    def stop(self) -> None:
        self.enqueue_call(self._stopped.set)
        self._thread.join()

    def enqueue_call(
        self,
        function: Callable[..., Awaitable[None] | None],
        *args: object,
    ) -> None:
        if not asyncio.iscoroutinefunction(function):
            self._asyncio_loop.call_soon_threadsafe(function, *args)
            return

        try:
            coroutine = function(*args)
            future = asyncio.run_coroutine_threadsafe(coroutine, self._asyncio_loop)
            future.add_done_callback(self._raise_coroutine_error)
        except TypeError as error:
            self.enqueue_raise(error)

    @staticmethod
    def _raise_coroutine_error(future: Future[None]) -> None:
        if not future.cancelled():
            if error := future.exception():
                raise error

    def enqueue_raise(self, error: Exception) -> None:
        self._asyncio_loop.call_soon_threadsafe(self._raise_error, error)

    @staticmethod
    def _raise_error(error: Exception) -> None:
        raise error
