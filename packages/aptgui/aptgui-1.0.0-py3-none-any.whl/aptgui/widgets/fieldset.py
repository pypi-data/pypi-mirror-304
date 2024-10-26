from ..collections import sequence
from ..layouts import Col, Row
from ..options import (
    Anchor,
    CardinalDistance,
    Sticky,
    horizontal_axis,
    vertical_axis,
)
from ..running import running
from ..utils import unique_name
from .frame import Frame


class FieldSet(Frame):
    def __init__(
        self,
        *rows_cols: Row | Col,
        anchor: Anchor = Anchor.TOPLEFT,
        margin: CardinalDistance = 0,
        padding: CardinalDistance = 0,
        sticky: Sticky = Sticky.ALL,
        text: str = "",
        underline: int = -1,
    ):
        self._grid_init(sequence(rows_cols))
        self.anchor = anchor
        self.margin = margin
        self.padding = padding
        self.sticky = sticky
        self.text = text
        self.underline = underline

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
                "ttk::labelframe", self._name,
                "-labelanchor", self.anchor.value,
                "-padding", self.padding,
                "-text", self.text,
                "-underline", self.underline,
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

        self._grid_create()
        self._update_on_setattr = True

    def _update(self) -> None:
        running.tcltk.enqueue_calls(
            (
                self._name, "configure",
                "-labelanchor", self.anchor.value,
                "-padding", self.padding,
                "-text", self.text,
                "-underline", self.underline,
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
        self._grid_delete()
        running.tcltk.enqueue_call("destroy", self._name)
        del self._col_span
        del self._row_span
        del self._col_index
        del self._row_index
        del self._name

    Anchor = Anchor
    Sticky = Sticky
