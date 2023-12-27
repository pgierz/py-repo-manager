import unittest

import ruamel.yaml

import py_repo_manager.line_column_utils as lc_utils

yaml = ruamel.yaml.YAML(typ="rt")


class TestGetLc(unittest.TestCase):
    def setUp(self):
        with open("./test_data/input_file.yaml", "r") as f:
            self.input_file = yaml.load(f)

    def test_get_lc(self):
        print(self.input_file)
        lc = lc_utils.get_lc(self.input_file, "")
        self.assertEqual((lc.line, lc.col), (0, 0))
        lc = lc_utils.get_lc(self.input_file, "data")
        self.assertEqual((lc.line, lc.col), (1, 2))
        lc = lc_utils.get_lc(self.input_file, "data.key8")
        self.assertEqual((lc.line, lc.col), (18, 4))
        lc = lc_utils.get_lc(self.input_file, "data.key8.0")
        self.assertEqual((lc.line, lc.col), (18, 6))
        lc = lc_utils.get_lc(self.input_file, "data.key8.0.inner_key2")
        self.assertEqual((lc.line, lc.col), (19, 6))
