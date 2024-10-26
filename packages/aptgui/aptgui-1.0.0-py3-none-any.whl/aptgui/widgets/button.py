from typing import Generic, TypeVar

from ..mixins import Widget
from ..options import (
    Callback,
    CardinalDistance,
    Sticky,
    horizontal_axis,
    vertical_axis,
)
from ..running import running
from ..utils import unique_name

T = TypeVar("T")


class Button(Generic[T], Widget):
    def __init__(
        self,
        *,
        margin: CardinalDistance = 0,
        on_press: Callback["Button[T]"] | None = None,
        sticky: Sticky = Sticky.ALL,
        text: str = "",
        value: T | None = None,
        underline: int = -1,
        width: int = 0,
    ):
        self.margin = margin
        self.on_press = on_press
        self.sticky = sticky
        self.text = text
        self.value = value
        self.underline = underline
        self.width = width

    def _create(
        self,
        parent_name: str,
        row_index: int = 0,
        col_index: int = 0,
        row_span: int = 1,
        col_span: int = 1,
    ) -> None:
        self._name = unique_name(self, parent_name=parent_name)
        self._row_index = row_index
        self._col_index = col_index
        self._row_span = row_span
        self._col_span = col_span

        running.tcltk.enqueue_calls(
            (
                "ttk::button", self._name,
                "-command", running.tcltk.command_for(self.on_press, self),
                "-text", self.text,
                "-underline", self.underline,
                "-width", self.width,
            ),
            (
                "grid", "configure", self._name,
                "-row", self._row_index,
                "-column", self._col_index,
                "-rowspan", self._row_span,
                "-columnspan", self._col_span,
                "-padx", horizontal_axis(self.margin),
                "-pady", vertical_axis(self.margin),
                "-sticky", self.sticky.value,
            ),
        )  # fmt: skip

        self._update_on_setattr = True

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                self._name, "configure",
                "-command", running.tcltk.command_for(self.on_press, self),
                "-text", self.text,
                "-underline", self.underline,
                "-width", self.width,
            ),
            (
                "grid", "configure", self._name,
                "-row", self._row_index,
                "-column", self._col_index,
                "-rowspan", self._row_span,
                "-columnspan", self._col_span,
                "-padx", horizontal_axis(self.margin),
                "-pady", vertical_axis(self.margin),
                "-sticky", self.sticky.value,
            ),
        )  # fmt: skip

    def _delete(self) -> None:
        self._update_on_setattr = False
        running.tcltk.enqueue_call("destroy", self._name)
        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._name

    Sticky = Sticky
