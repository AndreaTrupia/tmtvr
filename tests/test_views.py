import unittest
from unittest.mock import MagicMock
from tmtvr.views import create_view


class TestViews(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()

    def test_create_view(self):
        self.mock_db.get.return_value = None
        create_view(self.mock_db, 'test_design', 'test_view', 'function(doc) { emit(doc._id, null); }')

        self.mock_db.save.assert_called_once()
        args, _ = self.mock_db.save.call_args
        self.assertEqual(args[0]['_id'], '_design/test_design')
        self.assertIn('test_view', args[0]['views'])
        self.assertEqual(args[0]['views']['test_view']['map'], 'function(doc) { emit(doc._id, null); }')
