from models.BaseModel import BaseModel
import datetime

class Item(BaseModel):    
    def __init__(self,_DBCON, _id=None):
        self.fields = [
        ('name', None),
        ('collections', []),
        ('added', datetime.datetime.now()),
        ('userId', None),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)