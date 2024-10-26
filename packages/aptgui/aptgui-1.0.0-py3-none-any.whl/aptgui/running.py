from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App
    from .loops import Asyncio, TclTk


class _Running:
    _app: "App | None" = None
    _asyncio: "Asyncio | None" = None
    _tcltk: "TclTk | None" = None

    @property
    def app(self) -> "App":
        if not self._app:
            raise RuntimeError("there's no App running")

        return self._app

    @app.setter
    def app(self, app: "App") -> None:
        self._app = app

    @app.deleter
    def app(self) -> None:
        self._app = None

    @property
    def asyncio(self) -> "Asyncio":
        if not self._asyncio:
            raise RuntimeError("there's no Asyncio running")

        return self._asyncio

    @asyncio.setter
    def asyncio(self, asyncio: "Asyncio") -> None:
        self._asyncio = asyncio

    @asyncio.deleter
    def asyncio(self) -> None:
        self._asyncio = None

    @property
    def tcltk(self) -> "TclTk":
        if not self._tcltk:
            raise RuntimeError("there's no Tcl/Tk running")

        return self._tcltk

    @tcltk.setter
    def tcltk(self, tcltk: "TclTk") -> None:
        self._tcltk = tcltk

    @tcltk.deleter
    def tcltk(self) -> None:
        self._tcltk = None


running = _Running()
