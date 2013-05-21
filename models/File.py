from models.BaseModel import BaseModel
import datetime

class File(BaseModel):    
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('nicename', None),
        ('lowercasenicename', None),
        ('sysname', []),
        ('sessionId', None),
        ('added', datetime.datetime.now()),
        ('userId', None),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)

    def save(self):
    	self.lowercasenicename = self.nicename.lower()

        super(self.__class__, self).save()