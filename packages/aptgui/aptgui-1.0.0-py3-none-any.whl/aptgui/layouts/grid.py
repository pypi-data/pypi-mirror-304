from collections.abc import Iterable
from itertools import zip_longest

from ..collections import sequence
from .col import Col
from .row import Row


class Grid:
    _name: str

    def _grid_init(self, rows_cols: sequence[Row | Col]) -> None:
        self._rows = sequence(row for row in rows_cols if isinstance(row, Row))
        self._cols = sequence(col for col in rows_cols if isinstance(col, Col))

    def _grid_create(self) -> None:
        for index, row in enumerate(self._rows):
            row._create(self._name, index)

        for index, col in enumerate(self._cols):
            col._create(self._name, index)

    def _grid_update(self, old: sequence[Row | Col], new: sequence[Row | Col]) -> None:
        for index, (old_rc, new_rc) in enumerate(zip_longest(old, new, fillvalue=None)):
            if old_rc != new_rc:
                if old_rc:
                    old_rc._delete()
                if new_rc:
                    new_rc._create(self._name, index)

    def _grid_delete(self) -> None:
        for row in self._rows:
            row._delete()

        for col in self._cols:
            col._delete()

    @property
    def rows(self) -> sequence[Row]:
        return self._rows

    @rows.setter
    def rows(self, rows: Iterable[Row]) -> None:
        rows = sequence(rows)
        self._grid_update(self._rows, rows)
        self._rows = rows

    @property
    def cols(self) -> sequence[Col]:
        return self._cols

    @cols.setter
    def cols(self, cols: Iterable[Col]) -> None:
        cols = sequence(cols)
        self._grid_update(self._cols, cols)
        self._cols = cols
