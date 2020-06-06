
from database import Database

class Voter:
    
    def __init__(self, username, password, name=None, DOB=None, address=None, state=None, mobile=None, email=None, aadhaar=None, profilePic=None, status=None):
        self.username = username
        self.password = password
        self.name = name
        self.DOB = DOB
        self.address = address
        self.state = state
        self.mobile = mobile
        self.email = email
        self.aadhaar = aadhaar
        self.profilePic = profilePic
        self.status = status
    
    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'DOB': self.DOB,
            'address': self.address,
            'state': self.state,
            'mobile': self.mobile,
            'email': self.email,
            'aadhaar': self.aadhaar,
            'profilePic': self.profilePic,
            'status': self.status
        }

    def addVoter(self):
        Database.insert(collection='voter', data=self.json())

    @staticmethod
    def getVoter(query={}):
        return Database.find_one(collection='voter', query=query)

    @staticmethod
    def getVoters(query={}):
        return [voter for voter in Database.find(collection='voter', query=query)]

    @staticmethod
    def updateVoter(query={}, newval={}):
        return Database.update_one(collection='voter', query=query, newval=newval)
