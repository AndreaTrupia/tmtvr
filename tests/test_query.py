import unittest
from unittest.mock import MagicMock
from tmtvr.query import query_view


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()

    def test_query_view(self):
        query_view(self.mock_db, 'test_design', 'test_view', key='test_key')

        self.mock_db.view.assert_called_once_with('test_design/test_view', key='test_key')
