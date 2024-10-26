import asyncio
from collections.abc import Iterable

from .collections import setsequence
from .loops import Asyncio, TclTk
from .mixins import Repr
from .options import Callback
from .running import running
from .window import Window


class App(Repr):
    def __init__(
        self,
        *windows: Window,
        on_start: Callback["App"] | None = None,
    ):
        self._name = ""
        self._windows: setsequence[Window] = setsequence()
        self.on_start = on_start

        running.app = self
        running.asyncio = Asyncio(self._on_start)
        running.tcltk = TclTk()

        self.windows = windows  # type: ignore[assignment]

    async def _on_start(self) -> None:
        if asyncio.iscoroutinefunction(self.on_start):
            await self.on_start(self)
        elif self.on_start:
            self.on_start(self)

    def run(self) -> None:
        try:
            running.asyncio.start()
            running.tcltk.run()
        finally:
            running.asyncio.stop()

    @property
    def windows(self) -> setsequence[Window]:
        return self._windows

    @windows.setter
    def windows(self, new_windows: Iterable[Window]) -> None:
        new_windows = setsequence(new_windows)
        old_windows = self._windows

        for window in old_windows:
            if window not in new_windows:
                window._delete()

        for window in new_windows:
            if window not in old_windows:
                window._create(self._name)

        if not new_windows:
            running.tcltk.quit()

        self._windows = new_windows
