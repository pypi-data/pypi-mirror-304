from abc import ABC, abstractmethod

from .lifecycle import Lifecycle


class Widget(Lifecycle, ABC):
    _name: str

    @abstractmethod
    def _create(
        self,
        parent_name: str,
        row_index: int = 0,
        col_index: int = 0,
        row_span: int = 1,
        col_span: int = 1,
    ) -> None:
        pass
