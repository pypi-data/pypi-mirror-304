from collections.abc import Iterable
from typing import TypeVar

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


class ComboBox(Widget):
    def __init__(
        self,
        *,
        height: int = 0,
        justify: Justify = Justify.LEFT,
        margin: CardinalDistance = 0,
        on_change: Callback["ComboBox"] | None = None,
        state: WidgetState = WidgetState.NORMAL,
        sticky: Sticky = Sticky.LEFTRIGHT,
        value: str = "",
        values: Iterable[str] = tuple(),
        width: int = 0,
    ):
        self.height = height
        self.justify = justify
        self.margin = margin
        self.on_change = on_change
        self.state = state
        self.sticky = sticky
        self.value = value
        self._values = sequence(values)
        self.width = width

    @property
    def values(self) -> sequence[str]:
        return self._values

    @values.setter
    def values(self, values: Iterable[str]) -> None:
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
        self._variable_name = unique_name(
            self, parent_name=parent_name, type_name="variable"
        )
        self._row_index = row_index
        self._col_index = col_index
        self._row_span = row_span
        self._col_span = col_span
        self._last_on_change_command = running.tcltk.command_for(self.on_change, self)

        running.tcltk.enqueue_calls(
            (
                "set", self._variable_name, self.value,
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self.on_change, self),
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "ttk::combobox", self._name,
                "-height", self.height,
                "-justify", self.justify.value,
                "-state", self.state.value,
                "-textvariable", self._variable_name,
                "-values", tuple(self.values),
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

    def _read(self, combobox: "ComboBox") -> None:
        with self._suspend_update_on_setattr():
            self.value = str(running.tcltk.call(self._name, "get"))

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", self._last_on_change_command,
            ),
            (
                "set", self._variable_name, self.value,
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self.on_change, self),
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                self._name, "configure",
                "-height", self.height,
                "-justify", self.justify.value,
                "-state", self.state.value,
                "-values", tuple(self.values),
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

        self._last_on_change_command = running.tcltk.command_for(self.on_change, self)

    def _delete(self) -> None:
        self._update_on_setattr = False

        running.tcltk.enqueue_calls(
            (
                "destroy", self._name,
            ),
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", self._last_on_change_command,
            ),
            (
                "unset", self._variable_name,
            ),
        )  # fmt: skip

        del self._last_on_change_command
        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._variable_name
        del self._name

    Justify = Justify
    State = WidgetState
    Sticky = Sticky
