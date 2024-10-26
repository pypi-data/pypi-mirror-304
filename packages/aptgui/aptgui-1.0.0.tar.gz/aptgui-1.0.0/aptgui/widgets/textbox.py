from typing import TypeVar

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


class TextBox(Widget):
    def __init__(
        self,
        *,
        justify: Justify = Justify.LEFT,
        margin: CardinalDistance = 0,
        on_change: Callback["TextBox"] | None = None,
        show: str = "",
        state: WidgetState = WidgetState.NORMAL,
        sticky: Sticky = Sticky.LEFTRIGHT,
        value: str = "",
        width: int = 0,
    ):
        self.justify = justify
        self.margin = margin
        self.on_change = on_change
        self.show = show
        self.state = state
        self.sticky = sticky
        self.value = value
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
                "ttk::entry", self._name,
                "-justify", self.justify.value,
                "-show", self.show,
                "-state", self.state.value,
                "-textvariable", self._variable_name,
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

    def _read(self, textbox: "TextBox") -> None:
        with self._suspend_update_on_setattr():
            self.value = str(running.tcltk.call("set", self._variable_name))

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
                "-justify", self.justify.value,
                "-show", self.show,
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
