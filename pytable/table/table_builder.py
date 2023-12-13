from typing import List, Self
from pytable.table import Col, Table, Row, Body
from csv import DictReader


class TableBuilder:
    """
    The table module is order specific. You can provide a column schema with `Table.columns(Col(...))`.
    If no columns are provided, we use the first row as the header of the row. You can override this
    behavior by using `Table.config(headerless=True)`.
    """

    table = Table()

    @classmethod
    def columns(cls, *cols: List[Col]) -> type[Self]:
        """Set columns"""
        cls.table.columns = cols
        return cls

    @classmethod
    def body(cls, raw: list[Row]) -> type[Self]:
        """Set the body of the table"""
        # TODO: Allow adding to rows
        cls.table.body = Body(rows=raw)
        return cls

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

    @classmethod
    def from_csv(cls, file_path: str, with_head=False):
        """Method is like `Table.body()` but reads data from a csv file instead."""
        from_file = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = DictReader(file)

            for row in reader:
                from_file.append(dict(row).values())

        cls.table.body = Body(rows=from_file if with_head else from_file[1:])
        return cls
