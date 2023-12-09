import pymongo

class Database:
    def __init__(self) -> None:
        self.MONGODB_URL = 'mongodb+srv://sagar:sagar12345@cluster0.ryfnwqt.mongodb.net/?retryWrites=true&w=majority'
        self.DB_NAME = 'store'
    def get_client(self) -> pymongo.MongoClient:
        return pymongo.MongoClient(self.MONGODB_URL)
    def get_db_name(self) -> str:
        return self.DB_NAME

mongoDb= Database()
db = mongoDb.get_client()
db_name = mongoDb.get_db_name()