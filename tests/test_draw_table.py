import unittest

from pytable import Table, Col


class TestDrawTable(unittest.TestCase):
    def test_can_draw_table_with_header_configs(self):
        self.assertLogs(
            Table.columns(
                Col(label="First name"),
                Col(label="ID"),
                Col(label="D.O.Birth"),
            )
            .body(
                [
                    ["Bruce Wayne", "23232", "12/08/1988"],
                    ["Bruce Wayne", "23232", "12/08/1988"],
                    ["Bruce Wayne", "23232", "12/08/1988"],
                ]
            )
            .draw(),  # Should draw the table,
            """
+----------------+----------------+----------------+
|First name      |ID              |D.O.Birth       |
+================+================+================+
|Bruce Wayne     |23232           |12/08/1988      |
+----------------+----------------+----------------+
|Bruce Wayne     |23232           |12/08/1988      |
+----------------+----------------+----------------+
|Bruce Wayne     |23232           |12/08/1988      |
+----------------+----------------+----------------+
""",
        )

    def test_can_draw_table_without_col_configs(self):
        self.assertLogs(
            Table.body(
                [
                    ["First Name", "ID", "DOB"],
                    ["Bruce Wayne", "23232", "12/08/1988"],
                    ["Princess Diana of Themyscira", "47568", "12/08/1801"],
                    ["Clark Kent", "23232", "unknown"],
                ]
            ).draw(),
            """
+-------------------------------+--------+-------------+
|First Name                     |ID      |DOB          |
+===============================+========+=============+
|Bruce Wayne                    |23232   |12/08/1988   |
+-------------------------------+--------+-------------+
|Princess Diana of Themyscira   |47568   |12/08/1801   |
+-------------------------------+--------+-------------+
|Clark Kent                     |23232   |unknown      |
+-------------------------------+--------+-------------+
""",
        )
