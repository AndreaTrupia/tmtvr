import couchdb
import os


class Database:
    def __init__(self, host=None, port=None, user=None, password=None):
        host = host or os.environ.get('COUCHDB_HOST', 'localhost')
        port = port or os.environ.get('COUCHDB_PORT', 5984)
        user = user or os.environ.get('COUCHDB_USER', 'admin')
        password = password or os.environ.get('COUCHDB_PASSWORD', 'password')

        self.server = couchdb.Server(f'http://{user}:{password}@{host}:{port}/')

    def get_or_create(self, name):
        try:
            return self.server[name]
        except couchdb.http.ResourceNotFound:
            return self.server.create(name)

    def find(self, db_name, selector):
        db = self.get_or_create(db_name)
        return db.find({'selector': selector})
