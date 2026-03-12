import unittest
from unittest.mock import MagicMock
from datetime import datetime
from tmtvr.models import Model, TimestampedModel
from tmtvr.db import Database
from tmtvr.fields import StringField, IntegerField


class TestModel(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        Model.set_db(self.mock_db)

    def test_save(self):
        class TestModel(Model):
            name = StringField()
            age = IntegerField()

        model = TestModel(name='test', age=30)
        model.save()

        self.mock_db.save.assert_called_once()
        args, _ = self.mock_db.save.call_args
        self.assertIn('_id', args[0])
        self.assertEqual(args[0]['name'], 'test')
        self.assertEqual(args[0]['age'], 30)

    def test_get(self):
        class TestModel(Model):
            name = StringField()
            age = IntegerField()

        self.mock_db.get.return_value = {'_id': '123', 'name': 'test', 'age': 40}
        model = TestModel.get('123')

        self.assertIsInstance(model, TestModel)
        self.assertEqual(model._id, '123')
        self.assertEqual(model.name, 'test')
        self.assertEqual(model.age, 40)

    def test_timestamped_model(self):
        class TestTimestampedModel(TimestampedModel):
            name = StringField()

        model = TestTimestampedModel(name='test')
        model.save()

        self.mock_db.save.assert_called_once()
        args, _ = self.mock_db.save.call_args
        self.assertIn('created_at', args[0])
        self.assertIn('updated_at', args[0])
        self.assertIsInstance(datetime.fromisoformat(args[0]['created_at']), datetime)
        self.assertIsInstance(datetime.fromisoformat(args[0]['updated_at']), datetime)

    def test_filter(self):
        class TestModel(Model):
            name = StringField()
            age = IntegerField()

        self.mock_db.find.return_value = [
            {'_id': '1', 'name': 'John', 'age': 30},
            {'_id': '2', 'name': 'John', 'age': 25}
        ]

        results = TestModel.filter(name='John')

        self.mock_db.find.assert_called_once_with({'name': 'John'})
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], TestModel)
        self.assertEqual(results[0].name, 'John')
        self.assertEqual(results[0].age, 30)
        self.assertEqual(results[1].name, 'John')
        self.assertEqual(results[1].age, 25)
