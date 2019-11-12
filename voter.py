
from database import Database

class Voter:
    
    def __init__(self, username, password, name='name', DOB='dob', address='address', state='state', constituency='constituency', mobile='mobile', email='email', aadhaar='aadhar', profilePic='pic', status=False):
        self.username = username
        self.password = password
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
            'username': self.username,
            'password': self.password,
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