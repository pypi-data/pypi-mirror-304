from ..mixins import Widget
from ..options import (
    Anchor,
    CardinalDistance,
    Justify,
    Sticky,
    horizontal_axis,
    vertical_axis,
)
from ..running import running
from ..utils import unique_name


class Label(Widget):
    def __init__(
        self,
        *,
        anchor: Anchor = Anchor.LEFT,
        justify: Justify = Justify.LEFT,
        margin: CardinalDistance = 0,
        padding: CardinalDistance = 0,
        sticky: Sticky = Sticky.ALL,
        text: str = "",
        underline: int = -1,
        width: int = 0,
    ):
        self.anchor = anchor
        self.justify = justify
        self.margin = margin
        self.padding = padding
        self.sticky = sticky
        self.text = text
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
        self._name = unique_name(self, parent_name)
        self._row_index = row_index
        self._col_index = col_index
        self._row_span = row_span
        self._col_span = col_span

        running.tcltk.enqueue_calls(
            (
                "ttk::label", self._name,
                "-anchor", self.anchor.value,
                "-justify", self.justify.value,
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

        self._update_on_setattr = True

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                self._name, "configure",
                "-anchor", self.anchor.value,
                "-justify", self.justify.value,
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
        running.tcltk.enqueue_call("destroy", self._name)
        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._name

    Anchor = Anchor
    Justify = Justify
    Sticky = Sticky
