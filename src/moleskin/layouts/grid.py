from __future__ import annotations
from itertools import accumulate
from typing import Dict, List
from moleskin.layout import Layout, Size


class GridLayout(Layout):
    _singletons: Dict[
        int,
        Dict[
            int,
            GridLayout
        ]
    ] = {}

    def __new__(cls, columns: int, rows: int):
        try:
            by_rows = cls._singletons[columns]
        except KeyError:
            by_rows = cls._singletons[columns] = {}

        try:
            instance = by_rows[rows]
        except KeyError:
            instance = by_rows[rows] = super().__new__(cls)

        return instance

    def __init__(
            self,
            columns: int,
            rows: int
    ):
        self._columns = columns
        self._rows = rows

    @property
    def columns(self):
        return self._columns

    @property
    def rows(self):
        return self._rows

    @property
    def dimensions(self):
        return self._rows, self._columns

    def arrange(self, surface, child_sizes):
        rows: List[List[Size]] = [[] for _ in range(self._rows)]
        cols: List[List[Size]] = [[] for _ in range(self._columns)]
        for ordinal, size in enumerate(child_sizes[:self._columns * self._rows]):
            rows[ordinal // self._columns].append(size)
            cols[ordinal // self._rows].append(size)

        row_sizes: List[Size] = [(sum(width for width, _ in row), max(height for _, height in row)) for row in rows]
        col_sizes: List[Size] = [(max(width for width, _ in col), sum(height for _, height in col)) for col in cols]

        row_offsets = list(accumulate((height for _, height in row_sizes), initial=0))
        col_offsets = list(accumulate((width for width, _ in col_sizes), initial=0))

        return (
            (sum(width for width, _ in col_sizes), sum(height for _, height in row_sizes)),
            tuple(
                (row_offsets[ordinal // self._columns], col_offsets[ordinal // self._rows])
                for ordinal, _ in enumerate(child_sizes)
            )
        )


__all__ = ['GridLayout']
