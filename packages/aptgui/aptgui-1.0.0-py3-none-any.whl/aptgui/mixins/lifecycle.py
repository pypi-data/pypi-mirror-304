from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager

from ..options import get_option_names
from .repr import Repr


class Lifecycle(Repr, ABC):
    _update_on_setattr = False

    def __setattr__(self, name: str, value: object) -> None:
        super().__setattr__(name, value)
        if self._update_on_setattr and name in get_option_names(self):
            self._update()

    @contextmanager
    def _suspend_update_on_setattr(self) -> Iterator[None]:
        previous_update_on_setattr = self._update_on_setattr
        self._update_on_setattr = False
        try:
            yield
        finally:
            self._update_on_setattr = previous_update_on_setattr

    @abstractmethod
    def _create(self, parent_name: str) -> None:
        pass

    @abstractmethod
    def _update(self) -> None:
        pass

    @abstractmethod
    def _delete(self) -> None:
        pass
