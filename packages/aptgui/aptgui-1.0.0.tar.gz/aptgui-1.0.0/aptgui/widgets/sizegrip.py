from ..mixins import Widget
from ..options import CardinalDistance, Sticky, horizontal_axis, vertical_axis
from ..running import running
from ..utils import unique_name


class SizeGrip(Widget):
    def __init__(
        self,
        *,
        margin: CardinalDistance = 0,
        sticky: Sticky = Sticky.BOTTOMRIGHT,
    ):
        self.margin = margin
        self.sticky = sticky

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
                "ttk::sizegrip", self._name,
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
        running.tcltk.enqueue_call(
            "grid", "configure", self._name,
            "-row", self._row_index,
            "-column", self._col_index,
            "-rowspan", self._row_span,
            "-columnspan", self._col_span,
            "-padx", horizontal_axis(self.margin),
            "-pady", vertical_axis(self.margin),
            "-sticky", self.sticky.value,
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
