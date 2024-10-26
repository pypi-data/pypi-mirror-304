import contextlib
import sys
from collections.abc import Iterator

from .collections import sequence
from .layouts import Col, Grid, Row
from .loops.tcltk import Arguments
from .mixins import Lifecycle
from .options import Callback, CardinalDistance, WindowState
from .running import running
from .utils import unique_name
from .widgets import Frame

LINUX_PLATFORM = sys.platform == "linux"


def close(window: "Window") -> None:
    window.close()


def dont(window: "Window") -> None:
    pass


class Window(Grid, Lifecycle):
    def __init__(
        self,
        *rows_cols: Row | Col,
        framed: bool = True,
        on_close: Callback["Window"] = close,
        padding: CardinalDistance = 0,
        state: WindowState = WindowState.NORMAL,
        title: str = "",
    ):
        if framed:
            rows_cols = (
                Row(Frame(*rows_cols), weight=1),
                Col(weight=1),
            )

        self._grid_init(sequence(rows_cols))
        self.on_close = on_close
        self.state = state
        self.title = title

    def _create(self, parent_name: str) -> None:
        self._name = unique_name(self, parent_name=parent_name)

        running.tcltk.enqueue_calls(
            (
                "toplevel", self._name,
            ),
            (
                "wm", "state", self._name, WindowState.WITHDRAWN.value,
            ),
            (
                "wm", "title", self._name, self.title,
            ),
            (
                "wm", "protocol", self._name,
                "WM_DELETE_WINDOW", running.tcltk.command_for(self.on_close, self),
            ),
            (
                "bind", self._name,
                "<Configure>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<Map>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<Unmap>", running.tcltk.command_for(self._read, self),
            ),
        )  # fmt: skip

        self._grid_create()
        running.tcltk.enqueue_calls(*self._state_calls)
        self._update_on_setattr = True

    @property
    def _state_calls(self) -> Iterator[Arguments]:
        fullscreen = self.state == WindowState.FULLSCREEN
        maximized = self.state == WindowState.MAXIMIZED

        if LINUX_PLATFORM and maximized:
            yield ("wm", "state", self._name, WindowState.WITHDRAWN.value)
            yield ("update",)

        yield ("wm", "attributes", self._name, "-fullscreen", fullscreen)

        if LINUX_PLATFORM:
            yield ("wm", "attributes", self._name, "-zoomed", maximized)

        if fullscreen or LINUX_PLATFORM and maximized:
            yield ("wm", "state", self._name, WindowState.NORMAL.value)
        else:
            yield ("wm", "state", self._name, self.state.value)

    def _read(self, window: "Window") -> None:
        with self._suspend_update_on_setattr():
            with contextlib.suppress(AttributeError, RuntimeError):
                self.state = WindowState(running.tcltk.call("wm", "state", self._name))

                fullscreen = ("wm", "attributes", self._name, "-fullscreen")
                maximized = ("wm", "attributes", self._name, "-zoomed")

                if self.state == WindowState.NORMAL:
                    if bool(int(running.tcltk.call(*fullscreen))):  # type: ignore[call-overload]
                        self.state = WindowState.FULLSCREEN
                    elif LINUX_PLATFORM and bool(int(running.tcltk.call(*maximized))):  # type: ignore[call-overload]
                        self.state = WindowState.MAXIMIZED

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                "bind", self._name,
                "<Configure>", "",
            ),
            (
                "bind", self._name,
                "<Map>", "",
            ),
            (
                "bind", self._name,
                "<Unmap>", "",
            ),
            *self._state_calls,
            (
                "wm", "title", self._name, self.title,
            ),
            (
                "wm", "protocol", self._name,
                "WM_DELETE_WINDOW", running.tcltk.command_for(self.on_close, self),
            ),
            (
                "bind", self._name,
                "<Configure>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<Map>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<Unmap>", running.tcltk.command_for(self._read, self),
            ),
        )  # fmt: skip

    def _delete(self) -> None:
        self._update_on_setattr = False
        running.tcltk.enqueue_call(
            "wm", "state", self._name, WindowState.WITHDRAWN.value
        )
        self._grid_delete()
        running.tcltk.enqueue_call("destroy", self._name)
        del self._name

    def open(self) -> None:
        running.app.windows += self

    def close(self) -> None:
        running.app.windows -= self

    State = WindowState
