from collections.abc import Iterable
from types import EllipsisType

from ..collections import sequence
from ..mixins import Widget


class widgetsequence(sequence[Widget | EllipsisType | None]):
    def __init__(self, widgets: Iterable[Widget | EllipsisType | None], /):
        seen: set[Widget] = set()
        super().__init__(self._none_if_seen(widget, seen) for widget in widgets)

    @staticmethod
    def _none_if_seen(
        widget: Widget | EllipsisType | None,
        seen: set[Widget],
    ) -> Widget | EllipsisType | None:
        if widget in seen:
            return None
        else:
            if widget and widget != Ellipsis:
                seen.add(widget)  # type: ignore[arg-type]

            return widget

    def span(self, index: int) -> int:
        span = 1

        while index + span < len(self) and self[index + span] == Ellipsis:
            span += 1

        return span
