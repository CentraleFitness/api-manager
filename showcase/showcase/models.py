
from pymongo import MongoClient

class MongoClientHandler():
    def __init__(self, host: str='localhost', port: int=27017):
        self.client = MongoClient(host, port)

class MongoDB(MongoClientHandler):
    def __init__(self, db: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = self.client[db]

class MongoCollection(MongoDB):
    def __init__(self, collection: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = self.db[collection]
