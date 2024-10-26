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


class RadioButton(Generic[T], Widget):
    def __init__(
        self,
        *,
        checked: bool = False,
        group: str = "",
        margin: CardinalDistance = 0,
        on_press: Callback["RadioButton[T]"] | None = None,
        padding: CardinalDistance = 0,
        sticky: Sticky = Sticky.ALL,
        text: str = "",
        value: T | None = None,
        underline: int = -1,
        width: int = 0,
    ):
        self.checked = checked
        self.group = group
        self.margin = margin
        self.on_press = on_press
        self.padding = padding
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
        window_name = "." + self._name.split(".")[1]
        self._variable_name = f"{window_name}.radio_group.{self.group}"
        self._row_index = row_index
        self._col_index = col_index
        self._row_span = row_span
        self._col_span = col_span

        running.tcltk.enqueue_calls(
            (
                "eval",
                f"""
                if {{![info exists {{{self._variable_name}}}]}} {{
                    set {{{self._variable_name}}} none_checked
                }}
                if {{
                    {{{int(self.checked)}}}
                    && ${{{self._variable_name}}} != {{{self._name}}}
                }} {{
                    set {{{self._variable_name}}} {{{self._name}}}
                }}
                """,
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "ttk::radiobutton", self._name,
                "-value", self._name,
                "-variable", self._variable_name,
                "-command", running.tcltk.command_for(self.on_press, self),
                "-padding", self.padding,
                "-text", self.text,
                "-variable", self._variable_name,
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

    def _read(self, radiobutton: "RadioButton[T]") -> None:
        with self._suspend_update_on_setattr():
            self.checked = running.tcltk.call("set", self._variable_name) == self._name

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                "eval",
                f"""
                if {{
                    !{{{int(self.checked)}}}
                    && ${{{self._variable_name}}} == {{{self._name}}}
                }} {{
                    set {{{self._variable_name}}} none_checked
                }}
                if {{
                    {{{int(self.checked)}}}
                    && ${{{self._variable_name}}} != {{{self._name}}}
                }} {{
                    set {{{self._variable_name}}} {{{self._name}}}
                }}
                """,
            ),
            (
                "trace", "add",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            (
                self._name, "configure",
                "-command", running.tcltk.command_for(self.on_press, self),
                "-padding", self.padding,
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

        running.tcltk.enqueue_calls(
            (
                "destroy", self._name,
            ),
            (
                "trace", "remove",
                "variable", self._variable_name,
                "write", running.tcltk.command_for(self._read, self),
            ),
            # Don't unset the variable; other radio buttons may be using it.
            # (
            #     "unset", self._variable_name,
            # ),
        )  # fmt: skip

        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._variable_name
        del self._name

    Sticky = Sticky
