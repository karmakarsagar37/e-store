import pymongo

class Database:
    def __init__(self) -> None:
        self.MONGODB_URL = 'mongodb+srv://sagar:sagar12345@cluster0.ryfnwqt.mongodb.net/?retryWrites=true&w=majority'
        self.DB_NAME = 'store'
    def get_client(self) -> pymongo.MongoClient:
        return pymongo.MongoClient(self.MONGODB_URL).get_database(self.DB_NAME)
    
db = Database().get_client()