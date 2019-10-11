
from database import Database

class User:
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def json(self):
        return {
            'email': self.email,
            'password': self.password
        }

    def add_user(self):
        Database.insert(collection='users', data=self.json())
    
    @staticmethod
    def get_user(query={}):
        return Database.find_one(collection='users', query=query)