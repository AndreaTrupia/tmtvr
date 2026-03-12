import unittest
from unittest.mock import MagicMock, patch
from tmtvr.db import Database
import couchdb


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.mock_server = MagicMock()
        # We patch couchdb.Server to avoid real connections
        self.server_patcher = patch('couchdb.Server')
        self.mock_couchdb_server = self.server_patcher.start()
        self.mock_couchdb_server.return_value = self.mock_server

    def tearDown(self):
        self.server_patcher.stop()

    def test_get_or_create_existing(self):
        self.mock_server.__getitem__.return_value = 'existing_db'
        db = Database()
        result = db.get_or_create('test_db')
        self.assertEqual(result, 'existing_db')

    def test_get_or_create_new(self):
        self.mock_server.__getitem__.side_effect = couchdb.http.ResourceNotFound
        self.mock_server.create.return_value = 'new_db'
        db = Database()
        result = db.get_or_create('test_db')
        self.assertEqual(result, 'new_db')

    def test_init_with_args(self):
        Database('myhost', 1234, 'myuser', 'mypass')
        self.mock_couchdb_server.assert_called_with('http://myuser:mypass@myhost:1234/')

    @patch.dict('os.environ', {
        'COUCHDB_HOST': 'envhost',
        'COUCHDB_PORT': '5678',
        'COUCHDB_USER': 'envuser',
        'COUCHDB_PASSWORD': 'envpass'
    })
    def test_init_with_env_vars(self):
        Database()
        self.mock_couchdb_server.assert_called_with('http://envuser:envpass@envhost:5678/')

    def test_init_with_defaults(self):
        # Ensure environment variables are cleared for this test
        with patch.dict('os.environ', {}, clear=True):
            Database()
            self.mock_couchdb_server.assert_called_with('http://admin:password@localhost:5984/')
