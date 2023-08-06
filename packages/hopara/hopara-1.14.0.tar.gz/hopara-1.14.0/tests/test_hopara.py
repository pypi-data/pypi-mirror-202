import unittest
from unittest.mock import MagicMock
import logging

from hopara.hopara import Hopara
from hopara.table import Table


logging.getLogger('pyhopara').setLevel(logging.WARNING)


class HoparaCase(unittest.TestCase):
    def setUp(self):
        self.hopara = Hopara()
        self.hopara.config = MagicMock()
        self.hopara.config.get_dataset_url = lambda: 'https://test.hopara.py/'
        self.hopara.request = MagicMock()

    def test_urls(self):
        self.assertEqual(self.hopara.get_table_url(Table('table1')), r"https://test.hopara.py/table/table1/")
        self.assertEqual(self.hopara.get_row_url(Table('table1')), r"https://test.hopara.py/table/table1/row?dataSource=hopara")


if __name__ == '__main__':
    unittest.main()
