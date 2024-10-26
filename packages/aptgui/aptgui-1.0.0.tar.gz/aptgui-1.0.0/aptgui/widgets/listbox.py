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


class ListBox(Generic[T], Widget):
    def __init__(
        self,
        *,
        height: int = 0,
        justify: Justify = Justify.LEFT,
        label_maker: Callable[[T], str] = str,
        margin: CardinalDistance = 0,
        on_change: Callback["ListBox[T]"] | None = None,
        state: WidgetState = WidgetState.NORMAL,
        sticky: Sticky = Sticky.ALL,
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

    @property
    def _conditional_selection_set(self) -> tuple[str | int, ...]:
        if self.value is not None and self.values and self.value in self.values:
            return (self._name, "selection", "set", self.values.index(self.value))
        else:
            return (self._name, "selection", "clear", 0, "end")

    def _create(
        self,
        parent_name: str,
        row_index: int = 0,
        col_index: int = 0,
        row_span: int = 1,
        col_span: int = 1,
    ) -> None:
        self._name = unique_name(self, parent_name=parent_name)
        self._variable_name = unique_name(
            self, parent_name=parent_name, type_name="variable"
        )
        self._row_index = row_index
        self._col_index = col_index
        self._row_span = row_span
        self._col_span = col_span

        running.tcltk.enqueue_calls(
            (
                "set", self._variable_name, tuple(map(self.label_maker, self.values)),
            ),
            (
                "listbox", self._name,
                "-exportselection", 0,
                "-height", self.height,
                "-justify", self.justify.value,
                "-listvariable", self._variable_name,
                "-state", self.state.value,
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
            self._conditional_selection_set,
            (
                "bind", self._name,
                "<<ListboxSelect>>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<<ListboxSelect>>", f"+{running.tcltk.command_for(self.on_change, self)}",  # noqa: E501
            ),
        )  # fmt: skip

        self._update_on_setattr = True

    def _read(self, listbox: "ListBox[T]") -> None:
        with self._suspend_update_on_setattr():
            if selection_index := running.tcltk.call(self._name, "curselection"):
                self.value = self.values[int(str(selection_index))]

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                "set", self._variable_name, tuple(map(self.label_maker, self.values)),
            ),
            (
                self._name, "configure",
                "-height", self.height,
                "-justify", self.justify.value,
                "-state", self.state.value,
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
            self._conditional_selection_set,
            (
                "bind", self._name,
                "<<ListboxSelect>>", running.tcltk.command_for(self._read, self),
            ),
            (
                "bind", self._name,
                "<<ListboxSelect>>", f"+{running.tcltk.command_for(self.on_change, self)}",  # noqa: E501
            ),
        )  # fmt: skip

    def _delete(self) -> None:
        self._update_on_setattr = False

        running.tcltk.enqueue_calls(
            (
                "destroy", self._name,
            ),
            (
                "unset", self._variable_name,
            ),
        )  # fmt: skip

        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._variable_name
        del self._name

    Justify = Justify
    State = WidgetState
    Sticky = Sticky
