from ..mixins import Widget
from ..options import (
    Callback,
    CardinalDistance,
    Distance,
    Orientation,
    Sticky,
    horizontal_axis,
    vertical_axis,
)
from ..running import running
from ..utils import unique_name


class Slider(Widget):
    def __init__(
        self,
        *,
        length: Distance = 0,
        margin: CardinalDistance = 0,
        maximum: float = 1,
        minimum: float = 0,
        on_change: Callback["Slider"] | None = None,
        orientation: Orientation = Orientation.HORIZONTAL,
        sticky: Sticky = Sticky.LEFTRIGHT,
        value: float = 0,
    ):
        self.length = length
        self.margin = margin
        self.maximum = maximum
        self.minimum = minimum
        self.on_change = on_change
        self.orientation = orientation
        self.sticky = sticky
        self.value = value

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
            self, parent_name=self._name, type_name="variable"
        )
        self._row_index = row_index
        self._col_index = col_index
        self._row_span = row_span
        self._col_span = col_span

        running.tcltk.enqueue_calls(
            (
                "set", self._variable_name, self.value,
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "ttk::scale", self._name,
                "-command", running.tcltk.command_for(self.on_change, self),
                "-length", self.length,
                "-from", self.minimum,
                "-orient", self.orientation.value,
                "-to", self.maximum,
                "-variable", self._variable_name,
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

    def _read(self, slider: "Slider") -> None:
        with self._suspend_update_on_setattr():
            self.value = float(str(running.tcltk.call("set", self._variable_name)))

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "set", self._variable_name, self.value,
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                self._name, "configure",
                "-command", running.tcltk.command_for(self.on_change, self),
                "-length", self.length,
                "-from", self.minimum,
                "-orient", self.orientation.value,
                "-to", self.maximum,
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
                "unset", self._variable_name,
            ),
        )  # fmt: skip

        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._variable_name
        del self._name

    Orientation = Orientation
    Sticky = Sticky
