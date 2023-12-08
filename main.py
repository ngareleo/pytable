from dataclasses import dataclass
from typing import List
import numpy as np
from enum import Enum


class Alignment(Enum):
    CENTER = 0
    RIGHT = 1
    LEFT = 3


@dataclass
class Cell:
    size: int | None = None
    content: int | None = None


@dataclass
class Header:
    row: list[Cell]


@dataclass
class Body:
    rows: list[list[Cell]]


class Table:
    """Custom table just because I can ^-^"""

    # TODO: Reduce memory size of this table, alot of redundant attrs
    # TODO: Allow table updates by changing the body attr

    def __init__(self, header: Header, body: Body) -> None:
        self.header = header
        self.body = body

    def _draw_horizontal_border(self):
        sized_horizontal_lines = [
            "{:-<{size}}+".format("", size=cell.size) for cell in self.header.row
        ]
        return "".join(["+"] + sized_horizontal_lines)

    def _draw_header_content(self):
        sizes = []  # we get sizes from column schemas
        return "".join(
            ["|"]
            + [
                "{:{fill}<{size}}|".format(cell.content, fill=" ", size=cell.size)
                for cell in self.header.row
            ]
            + ["\n"]
            + ["+"]  # start of the bottom border that uses = instead of -
            + ["{:=<{size}}+".format("", size=cell.size) for cell in self.header.row]
        )

    def _draw_body(self):
        return [
            "".join(
                ["|"]
                + [
                    "{:{fill}<{size}}|".format(cell.content, fill=" ", size=cell.size)
                    for cell in row
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

    @classmethod
    def draw_from_list(cls, content: List[List[str]]):
        """Assumes the first array is the header"""
        cells = np.transpose([[Cell(content=cell) for cell in row] for row in content])

        for col in cells:
            width = len(max(col, key=lambda a: len(a.content)).content) + 3
            for cell in col:
                cell.size = width
        [head, *rest] = list(np.transpose(cells))
        table = Table(header=Header(row=head), body=Body(rows=rest))
        table.draw_table()

    @classmethod
    def add_row(cls, content: List[List[str]]):
        """This method expects"""
        pass


if __name__ == "__main__":
    s = [
        ["Name", "Org", "Age"],
        ["Lead Jason", "Med", "23"],
        ["Ruthy Ljarson", "Eng", "23"],
    ]
    Table.draw_from_list(s)
