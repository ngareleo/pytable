import numpy as np
from enum import Enum
from typing import TypeVar, Type

type T = TypeVar("T", str, int, float)
type Row = Type[list[str]]


class Alignment(Enum):
    CENTER = 0
    RIGHT = 1
    LEFT = 3


class Col:
    max_width = 16
    width = max_width

    def __init__(
        self,
        name: str,
        label: str,
    ) -> None:
        self.name = name
        self.label = label


class Header:
    def __init__(self, cols: list[Row]) -> None:
        self.cols = cols


class Body:
    def __init__(self, rows: list[Row] = None) -> None:
        self.rows = rows

    def get_col_sizes(self, cols: list[Col]) -> list[Col]:
        pass


class Table:
    """
    The table module is order specific. You can provide a column schema with columns(Col(...)).
    If no columns are provided, we use the first row as the header of the row. You can override this
    behavior by using config(headerless=True).

    The body, which is a 2d array of strings should be in the same order as the Col() objects in the header.

    TODO: Later we will allow use of keys and allow users to use dicts instead.
    """

    default_limit = 50

    def __init__(
        self, columns: list[Col] = None, body: Body = None, limit=default_limit
    ) -> None:
        self.columns = columns
        self.body = body
        self.limit = limit

    def _draw_horizontal_border(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        # Always called after self.draw()
        # No checks required
        sized_horizontal_lines = [
            "{:-<{size}}+".format("", size=col.width) for col in self.columns
        ]
        return "".join(["+"] + sized_horizontal_lines)

    def _draw_header_content(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        return "".join(
            ["|"]
            + [
                "{:{fill}<{size}}|".format(col.label, fill=" ", size=col.width)
                for col in self.columns
            ]
            + ["\n"]
            + ["+"]  # start of the bottom border that uses = instead of -
            + ["{:=<{size}}+".format("", size=col.width) for col in self.columns]
        )

    def _draw_body(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        if not self.body:
            raise ValueError("body not provided")

        col_widths = [col.width for col in self.columns]
        return [
            "".join(
                ["|"]
                + [
                    "{:{fill}<{size}}|".format(cell, fill=" ", size=w)
                    for w, cell in zip(col_widths, row)
                ]
                + ["\n", self._draw_horizontal_border()]
            )
            for row in self.body.rows
        ]

    def draw_table(self):
        print(
            self._draw_horizontal_border(),
            self._draw_header_content(),
            *self._draw_body(),
            sep="\n",
        )

    def get_configs_from_head(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        if not self.body:
            raise ValueError("body not provided")

        [head, *_] = self.body.rows
        self.columns = [Col(label=col) for col in head]
        for w, col in zip(self._get_col_widths(), self.columns):
            col.width = w

    def _get_col_widths(self) -> list[int]:
        """Assumes the first array is the header"""
        cells = np.transpose(self.body.rows)
        return [len(max(col, key=lambda a: len(a))) + 3 for col in cells]
