import unittest
from pytable.table import Table


class TestConfigChanges(unittest.TestCase):
    def test_config_changes_from_constructor(self):
        instance = Table(max_col_width=90)
        self.assertEqual(instance.config.max_col_width, 90)

    def test_config_changes_from_constructor(self):
        instance = Table()
        instance.set_configs_from_kwargs(max_col_width=90)
        self.assertEqual(instance.config.max_col_width, 90)


if __name__ == "__main__":
    unittest.main()
