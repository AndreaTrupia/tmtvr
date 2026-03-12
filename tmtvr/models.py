import uuid
from datetime import datetime, timezone
from .db import Database
from .fields import Field, DateTimeField


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        attrs['_fields'] = fields
        
        meta = attrs.get('Meta')
        if meta:
            attrs['_table_name'] = getattr(meta, 'table_name', None)
        
        return super().__new__(cls, name, bases, attrs)


class Model(metaclass=ModelMeta):
    _db = None
    _server = None
    _id = None
    _rev = None
    _table_name = None

    def __init__(self, **kwargs):
        for key, value in self._fields.items():
            setattr(self, key, kwargs.get(key, value.default))
        
        if '_id' in kwargs:
            self._id = kwargs['_id']
        else:
            self._id = str(uuid.uuid4())
        
        if '_rev' in kwargs:
            self._rev = kwargs['_rev']


    @classmethod
    def set_db(cls, db):
        """Legacy: set a specific couchdb database instance."""
        cls._db = db

    @classmethod
    def set_server(cls, server: Database):
        """Set the tmtvr Database server instance."""
        cls._server = server

    @classmethod
    def get_db(cls):
        if cls._table_name and cls._server:
            return cls._server.get_or_create(cls._table_name)
        if cls._db:
            return cls._db
        raise Exception("Database not set. Use Model.set_server() or Model.set_db()")

    def save(self):
        db = self.get_db()
        
        data = {key: getattr(self, key) for key in self._fields}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

        data['_id'] = self._id
        if self._rev:
            data['_rev'] = self._rev

        db.save(data)
        if '_rev' in data:
            self._rev = data['_rev']


    @classmethod
    def get(cls, doc_id):
        db = cls.get_db()
        doc = db.get(doc_id)
        if doc:
            return cls(**doc)
        return None

    @classmethod
    def filter(cls, **kwargs):
        """
        Filters documents based on the provided criteria using Mango queries.
        Example: MyModel.filter(name="John", age=30)
        """
        if cls._server is None and cls._db is None:
             raise Exception("Database not set. Use Model.set_server() or Model.set_db()")

        selector = kwargs
        
        if cls._table_name and cls._server:
             results = cls._server.find(cls._table_name, selector)
        elif cls._db:
             # Fallback for legacy set_db usage, assuming db object has find method (couchdb-python does)
             results = cls._db.find(selector)
        else:
             return []

        return [cls(**doc) for doc in results]


class TimestampedModel(Model):
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._fields.update({
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })


    def save(self):
        self.updated_at = datetime.now(timezone.utc)
        if not self._rev:
            self.created_at = datetime.now(timezone.utc)
        super().save()
