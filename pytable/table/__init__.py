import numpy as np
from typing import TypeVar, Any
from functools import reduce
from pytable.table.column import Alignment, Col
from pytable.utils import cutAtSpace

type T = TypeVar("T", str, int, float)
type Row = list[str]
type DictRow = dict[str, str]


class Header:
    def __init__(self, cols: list[Row]) -> None:
        self.cols = cols


class Body:
    def __init__(self, rows: list[Row] = None) -> None:
        self.rows = rows

    def remove_first_row(self) -> None:
        self.rows.pop(0)


class TableConfigs:
    """These are configurations that apply globally to all entities. They can be edited by using `Table.config(**kwargs)`"""

    headerless = False
    max_width = None  # Initially all cols can stretch as much
    align = Alignment.LEFT


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
        # This constructor creates the default table representation
        # This module is built to provide hook and  extension of one core behavior.
        # Simply, we have this process of creating tables on a cli by printing lines in order
        # row by row
        # This module should allow us to gain as much control during this process and therefore `add features`
        # It then should in no way change the process

        self.columns = columns
        self.body = body
        self.limit = limit
        self.config = TableConfigs()
        self.edit_global_table_configs(**configs)

    def edit_global_table_configs(self, **configs):
        for key, value in configs.items():
            if (
                key.startswith("_")
                or key.endswith("_")
                or key not in self.config.__dir__()
            ):
                raise ValueError(f"Config {key} does not exist")

            if key in Col.__dict__.keys():
                self._apply_global_col_config(key, value)
            self.config.__setattr__(key, value)

    def _apply_global_col_config(self, k: str, v: Any):
        if self.columns:
            for col in self.columns:
                col.__setattr__(k, v)

    #################################################################
    ################## Render logic #################################
    #################################################################

    def _render_horizontal_border(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        # Always called after self.draw()
        # No checks required
        sized_horizontal_lines = [
            "{:-<{size}}+".format("", size=col.width) for col in self.columns
        ]
        return "".join(["+"] + sized_horizontal_lines)

    def _render_header_content(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        return "".join(
            ["|"]
            + [
                "{:{fill}{align}{size}}|".format(
                    col.label, fill=" ", size=col.width, align=col.align
                )
                for col in self.columns
            ]
            + ["\n"]
            + ["+"]  # start of the bottom border that uses = instead of -
            + ["{:=<{size}}+".format("", size=col.width) for col in self.columns]
        )

    def _render_single_row(self, row: Row):
        drawable_cells = []
        rest_cells = []
        for rule, cell in zip(self.columns, row):
            drawable, rest = cutAtSpace(cell, rule.width)
            drawable_cells.append(drawable)
            rest_cells.append(rest)

        # Look ahead if we need next line
        will_not_execute_next = (
            reduce(lambda a, b: a.strip() + b.strip(), rest_cells) == ""
        )
        line = "".join(
            ["|"]
            + [
                "{:{fill}{align}{size}}|".format(
                    cell, fill=" ", size=col.width, align=col.align
                )
                for col, cell in zip(self.columns, drawable_cells)
            ]
            + ["\n"]
        )

        if will_not_execute_next:
            return line + self._render_horizontal_border()
        else:
            return line + "\n" + self._render_single_row(rest_cells)

    def _render_body(self):
        if not self.columns:
            raise ValueError("Headers not defined")

        if not self.body:
            raise ValueError("body not provided")

        return [self._render_single_row(row) for row in self.body.rows]

    def render_table(self):
        header = "".join(
            [self._render_horizontal_border(), "\n", self._render_header_content()]
        )
        print(
            self._render_horizontal_border() if self.config.headerless else header,
            *self._render_body(),
            sep="\n",
        )

    ########################################################
    ################### Utils ##############################
    ########################################################

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
        return [len(max(col, key=len)) + 3 for col in cells]
