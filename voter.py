
from database import Database

class Voter:
    
    def __init__(self, name, DOB, address, state, constituency, mobile, email, aadhaar, profilePic, status=False):
        self.name = name
        self.DOB = DOB
        self.address = address
        self.state = state
        self.constituency = constituency
        self.mobile = mobile
        self.email = email
        self.aadhaar = aadhaar
        self.profilePic = profilePic
        self.status = status
    
    def json(self):
        return {
            'name': self.name,
            'DOB': self.DOB,
            'address': self.address,
            'state': self.state,
            'constituency': self.constituency,
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