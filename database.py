
import pymongo

class Database:
    #client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    client = pymongo.MongoClient("mongodb+srv://sahil:sahilpass@sahil0-qjtu7.mongodb.net/test?retryWrites=true&w=majority")
    db = client['vote4u']

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert(data)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def find(collection, query):
        return Database.db[collection].find(query)

    @staticmethod
    def update(collection, query):
        return Database.db[collection].update(query)
