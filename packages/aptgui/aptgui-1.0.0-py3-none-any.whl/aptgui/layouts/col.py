from collections.abc import Iterable
from types import EllipsisType

from ..mixins import Lifecycle, Widget
from ..running import running
from .widgetsequence import widgetsequence


class Col(Lifecycle):
    def __init__(self, *widgets: Widget | EllipsisType | None, weight: int = 0):
        self._widgets = widgetsequence(widgets)
        self.weight = weight

    def _create(self, name: str, index: int = 0) -> None:
        self._name = name
        self._index = index
        self._update()

        for row_index, widget in enumerate(self.widgets):
            if isinstance(widget, Widget):
                row_span = self.widgets.span(row_index)
                col_span = 1
                widget._create(self._name, row_index, self._index, row_span, col_span)

        self._update_on_setattr = True

    def _update(self) -> None:
        running.tcltk.enqueue_call(
            "grid", "columnconfigure", self._name, self._index,
            "-weight", self.weight,
        )  # fmt: skip

    def _delete(self) -> None:
        self._update_on_setattr = False

        for widget in self.widgets:
            if isinstance(widget, Widget):
                widget._delete()

        del self._index
        del self._name

    @property
    def widgets(self) -> widgetsequence:
        return self._widgets

    @widgets.setter
    def widgets(self, widgets: Iterable[Widget | EllipsisType | None]) -> None:
        widgets = widgetsequence(widgets)
        name = self._name
        index = self._index
        self._delete()
        self._widgets = widgets
        self._create(name, index)
