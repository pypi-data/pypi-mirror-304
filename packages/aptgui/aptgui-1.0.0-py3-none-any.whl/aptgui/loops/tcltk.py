from _tkinter import create as create_tcltk_loop
from collections import deque
from functools import cache
from typing import TypeAlias

from ..options import Callback, CallbackArg
from ..running import running
from ..utils import unique_name

Scalar: TypeAlias = bool | int | float | str | None
Argument: TypeAlias = Scalar | tuple[Scalar, ...]
Arguments: TypeAlias = tuple[Argument, ...]


class TclTk:
    def __init__(self) -> None:
        self._call_queue: deque[Arguments] = deque()
        self._flush_pending = False
        self._tcltk_loop = create_tcltk_loop()
        self._tcltk_loop.call("wm", "withdraw", ".")
        self._tcltk_loop.call("option", "add", "*tearOff", False)
        self._tcltk_loop.createcommand("flush_calls", self._flush_calls)

    def run(self) -> None:
        self._tcltk_loop.mainloop()

    def quit(self) -> None:
        self._tcltk_loop.quit()

    def call(self, *args: Argument) -> object:
        return self._tcltk_loop.call(*args)

    def enqueue_call(self, *args: Argument) -> None:
        self._call_queue.append(args)
        if not self._flush_pending:
            self._flush_pending = True
            self._tcltk_loop.call("after", "0", "flush_calls")

    def enqueue_calls(self, *args: Arguments) -> None:
        self._call_queue.extend(args)
        if not self._flush_pending:
            self._flush_pending = True
            self._tcltk_loop.call("after", "0", "flush_calls")

    def _flush_calls(self) -> None:
        try:
            while self._call_queue:
                args = self._call_queue.popleft()
                self._tcltk_loop.call(*args)
        except Exception as error:
            running.asyncio.enqueue_raise(error)
        finally:
            self._flush_pending = False

    @cache
    def command_for(
        self, callback: Callback[CallbackArg] | None, arg: CallbackArg
    ) -> str:
        if not callback:
            return ""

        def enqueue_call(*_: object) -> None:
            running.asyncio.enqueue_call(callback, arg)

        command_name = unique_name(enqueue_call, type_name="command")
        self._tcltk_loop.createcommand(command_name, enqueue_call)
        return command_name
