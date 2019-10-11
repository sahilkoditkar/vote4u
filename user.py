
from database import Database

class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def json(self):
        return {
            'username': self.userame,
            'password': self.password
        }

    def add_user(self):
        Database.insert(collection='users', data=self.json())
    
    @staticmethod
    def get_user(query={}):
        return Database.find_one(collection='users', query=query)
