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
    default_max_width = 16

    def __init__(
        self,
        label: str,  # The label to display on the header
        width=default_max_width,  # If width is not provided it will not be wider than max-width
        max_width=default_max_width,  # Max width of a single column, Default behavior is overflow
    ) -> None:
        self.label = label
        self.width = width
        self.max_width = max_width


class Header:
    def __init__(self, cols: list[Row]) -> None:
        self.cols = cols


class Body:
    def __init__(self, rows: list[Row] = None) -> None:
        self.rows = rows

    def get_col_sizes(self, cols: list[Col]) -> list[Col]:
        pass

    def remove_first_row(self) -> None:
        self.rows.pop(0)


class TableConfigs:
    max_col_width: str = 20


class Table:
    """Internal implementation of table"""

    default_limit = 50

    def __init__(
        self,
        columns: list[Col] = None,
        body: Body = None,
        limit=default_limit,
        **configs,
    ) -> None:
        self.columns = columns
        self.body = body
        self.limit = limit
        self.config = TableConfigs()
        self.set_configs_from_kwargs(**configs)

    def set_configs_from_kwargs(self, **configs):
        for key, value in configs.items():
            if (
                key.startswith("__")
                or key.endswith("__")
                or key not in self.config.__dir__()
            ):
                pass

            self.config.__setattr__(key, value)

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

    def get_cols_configs_from_head(self):
        if not self.body:
            raise ValueError("body not provided")

        [head, *_] = self.body.rows
        self.columns = [Col(label=col) for col in head]
        for w, col in zip(self._get_col_widths(), self.columns):
            col.width = w

        # remove the first col from body
        self.body.remove_first_row()

    def _get_col_widths(self) -> list[int]:
        """Assumes the first array is the header"""
        cells = np.transpose(self.body.rows)
        return [len(max(col, key=lambda a: len(a))) + 3 for col in cells]
