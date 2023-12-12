from typing import List, Self
from pytable.table import Col, Table, Row, Body


class TableBuilder:
    """
    The table module is order specific. You can provide a column schema with columns(Col(...)).
    If no columns are provided, we use the first row as the header of the row. You can override this
    behavior by using config(headerless=True).
    The body, which is a 2d array of strings should be in the same order as the Col() objects in the header.
    """

    table = Table()

    @classmethod
    def columns(cls, *cols: List[Col]) -> type[Self]:
        cls.table.columns = cols
        return cls

    @classmethod
    def body(cls, raw: list[Row]) -> type[Self]:
        cls.table.body = Body(rows=raw)
        return cls

    @classmethod
    def limit(cls, limit: int) -> type[Self]:
        cls.table.limit = limit
        return cls

    @classmethod
    def config(cls, **configs) -> type[Self]:
        cls.table.set_configs_from_kwargs(**configs)
        return cls

    @classmethod
    def draw(cls) -> None:
        """
        Terminal method. You cannot edit the table after drawing it.
        To reuse table configs look at the Table module.
        """
        # Terminal method of the builder

        if not cls.table.body:
            raise ValueError(
                "No table body was provided. Use Table.body([[]]) to declare a body"
            )

        if not cls.table.columns:
            cls.table.get_cols_configs_from_head()

        cls.table.draw_table()
        cls.table = Table()

    @classmethod
    def snip(cls, draw=False) -> None:
        """
        Terminal method. It snips the table and starts a new table.
        """
        if draw:
            # @leolint: allow this dirty move
            print("\n", cls.table._draw_horizontal_border(), "\n\n")
        cls.table = Table()
