from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

from ..collections import sequence
from ..mixins import Widget
from ..options import (
    Callback,
    CardinalDistance,
    Justify,
    Sticky,
    WidgetState,
    horizontal_axis,
    vertical_axis,
)
from ..running import running
from ..utils import unique_name

T = TypeVar("T")


class DropDown(Generic[T], Widget):
    def __init__(
        self,
        *,
        height: int = 0,
        justify: Justify = Justify.LEFT,
        label_maker: Callable[[T], str] = str,
        margin: CardinalDistance = 0,
        on_change: Callback["DropDown[T]"] | None = None,
        state: WidgetState = WidgetState.NORMAL,
        sticky: Sticky = Sticky.LEFTRIGHT,
        value: T | None = None,
        values: Iterable[T] = tuple(),
        width: int = 0,
    ):
        self.height = height
        self.justify = justify
        self.label_maker = label_maker
        self.margin = margin
        self.on_change = on_change
        self.state = state
        self.sticky = sticky
        self.value = value
        self._values = sequence(values)
        self.width = width

    @property
    def values(self) -> sequence[T]:
        return self._values

    @values.setter
    def values(self, values: Iterable[T]) -> None:
        self._values = sequence(values)

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

        if self.state == WidgetState.DISABLED:
            state = WidgetState.DISABLED
        else:
            state = WidgetState.READONLY

        value = self.label_maker(self.value) if self.value is not None else ""

        running.tcltk.enqueue_calls(
            (
                "ttk::combobox", self._name,
                "-height", self.height,
                "-justify", self.justify.value,
                "-state", state.value,
                "-values", tuple(map(self.label_maker, self.values)),
                "-width", self.width,
            ),
            (
                self._name, "set", value,
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
            (
                "bind", self._name,
                "<<ComboboxSelected>>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<<ComboboxSelected>>", f"+{running.tcltk.command_for(self.on_change, self)}",  # noqa: E501
            ),
        )  # fmt: skip

        self._update_on_setattr = True

    def _read(self, dropdown: "DropDown[T]") -> None:
        with self._suspend_update_on_setattr():
            running.tcltk.call("selection", "clear")
            self.value = self.values[int(running.tcltk.call(self._name, "current"))]  # type: ignore[call-overload]

    def _update(self) -> None:
        if self.state == WidgetState.DISABLED:
            state = WidgetState.DISABLED
        else:
            state = WidgetState.READONLY

        value = self.label_maker(self.value) if self.value is not None else ""

        running.tcltk.enqueue_calls(
            (
                self._name, "configure",
                "-height", self.height,
                "-justify", self.justify.value,
                "-state", state.value,
                "-values", tuple(map(self.label_maker, self.values)),
                "-width", self.width,
            ),
            (
                self._name, "set", value,
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
            (
                "bind", self._name,
                "<<ComboboxSelected>>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<<ComboboxSelected>>", f"+{running.tcltk.command_for(self.on_change, self)}",  # noqa: E501
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

    Justify = Justify
    State = WidgetState
    Sticky = Sticky
