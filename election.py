
from database import Database

class Election:

    def __init__(self, title, description, date, starttime, endtime, candidates):
        self.title = title
        self.description = description
        self.date = date
        self.starttime = starttime
        self.endtime = endtime
        self.candidates = candidates
    
    def json(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'starttime': self.starttime,
            'endtime': self.endtime,
            'candidates': self.candidates
        }

    def setElection(self):
        Database.insert(collection='election', data=self.json())
    
    @staticmethod
    def getElection(query={}):
        return Database.find_one(collection='election', query=query)

    @staticmethod
    def getElections(query={}):
        return [election for election in Database.find(collection='election', query=query)]

    @staticmethod
    def updateElection(query={}, newval={}):
        return Database.update_one(collection='election', query=query, newval=newval)
