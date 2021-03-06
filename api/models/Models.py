from models.BaseModel import BaseModel
import datetime

class File(BaseModel):    
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('nicename', None),
        ('lowercasenicename', None),
        ('sysname', None),
        ('sessionId', None),
        ('added', datetime.datetime.now()),
        ('userId', None),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)

    def save(self):
    	self.lowercasenicename = self.nicename.lower()

        super(self.__class__, self).save()



class Item(BaseModel):    
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('name', None),
        ('files', []),
        ('collections', []),
        ('added', datetime.datetime.now()),
        ('userId', None),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)

    def save(self):
    	self.lowercasename = self.name.lower()

        super(self.__class__, self).save()




class Collection(BaseModel):    
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('name', None),
        ('lowercasename', None),
        ('slug', None),
        ('added', datetime.datetime.now()),
        ('userId', None),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)

    def save(self):
    	self.lowercasename = self.name.lower()
        self.slug = self.lowercasename.replace(' ','-')

        super(self.__class__, self).save()