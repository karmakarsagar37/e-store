import pymongo
import os
import urllib.parse

class Database:
    def __init__(self) -> None:
        self.username = urllib.parse.quote_plus(str(os.environ.get("DB_USERNAME")))
        self.password = urllib.parse.quote_plus(str(os.environ.get("DB_PASSWORD")))
        self.MONGODB_URL = f'mongodb+srv://{self.username}:{self.password}@web.pqkfpsb.mongodb.net/?retryWrites=true&w=majority'
        self.DB_NAME = os.environ.get('DB_NAME')
    def get_client(self) -> pymongo.MongoClient:
        return pymongo.MongoClient(self.MONGODB_URL)
    def get_db_name(self) -> str:
        return self.DB_NAME

mongoDb= Database()
db = mongoDb.get_client()
db_name = mongoDb.get_db_name()