from typing import List, Self
from pytable.table import Col, DictRow, Table, Row, Body
from csv import DictReader
from json import load


class DictAdapter:
    pass


class TableBuilder:
    """
    The table module is order specific. You can provide a column schema with `Table.columns(Col(...))`.
    If no columns are provided, we use the first row as the header of the row. You can override this
    behavior by using `Table.config(headerless=True)`.
    """

    table = Table()

    @classmethod
    def columns(cls, *cols: Col) -> type[Self]:
        """Set columns"""
        keys = [col.key for col in cols]
        if None in keys and not None in keys:
        cls.table.columns = cols
        return cls

    @classmethod
    def body(cls, raw: list[Row]) -> type[Self]:
        """Set the body of the table"""
        # TODO: Allow adding to rows
        cls.table.body = Body(rows=raw)
        return cls

    def json(cls, raw: list[DictRow], derive_headers=False) -> type[Self]:
        # Convert this object data into arrays
        if len(raw) == 0:
            raise ValueError("Passed an empty file")
        ls = [item.values() for item in raw]

        cls.table.body = Body(rows=ls)

    @classmethod
    def limit(cls, limit: int) -> type[Self]:
        """Set a limit of how many rows to print"""
        cls.table.limit = limit
        return cls

    @classmethod
    def config(cls, **configs) -> type[Self]:
        """Allows to edit global table configs"""
        cls.table.edit_global_table_configs(**configs)
        return cls

    @classmethod
    def draw(cls) -> None:
        """
        Terminal method. You cannot edit the table after drawing it.
        To reuse table configs look at the `Table` module.
        """
        # Terminal method of the builder

        if not cls.table.body:
            raise ValueError(
                "No table body was provided. Use Table.body([[]]) to declare a body"
            )

        if not cls.table.columns:
            cls.table.get_cols_configs_from_head()

        cls.table.render_table()
        cls.table = Table()

    @classmethod
    def snip(cls, draw=False) -> None:
        """
        Terminal method. It snips the table and starts a new table.
        """
        if draw:
            # @leolint: allow this dirty move
            print("\n", cls.table._render_horizontal_border(), "\n\n")
        cls.table = Table()

    # TODO: Merge into one function

    @classmethod
    def from_csv_file(cls, file_path: str, derive_headers=True):
        """
        Method is like `Table.body()` but reads data from a csv file instead.
        If no columns are provided through the `Table.columns()`, the column titles will be derived from the head of the csv file.
        By default, the table will draw all columns. So inorder to limit the size of the table, it is recommended that use:
        `Table.columns(Col(name: {key}))`. Replace key with the column title to show. The two values should match or else a `ValueError` will be raised.

        `derive_headers` -- Whether to use the labels as labels on the table. Default: `True`.
        """
        from_file = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = DictReader(file)
            for row in reader:
                from_file.append(dict(row).values())

        if len(from_file) == 0:
            raise ValueError("File has no content to display")

        cls.table.body = Body(rows=from_file)

        return cls

    @classmethod
    def read_json_file(cls, file_path):
        with open(file_path, "r", encoding="utf-8") as json_file:
            data_list = load(json_file)
            cls.table.body = Body(rows=data_list)

        return cls
