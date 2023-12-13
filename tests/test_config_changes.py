import unittest
from pytable.table import Table, Col


class TestConfigChanges(unittest.TestCase):
    def test_config_changes_from_constructor(self):
        instance = Table(max_width=90)
        self.assertEqual(instance.config.max_width, 90)

    def test_config_changes_using_object(self):
        instance = Table()
        instance.edit_global_table_configs(max_width=90)
        self.assertEqual(instance.config.max_width, 90)
        col = Col(label="Name")
        self.assertEqual(col.default_max_width, 90)


if __name__ == "__main__":
    unittest.main()
