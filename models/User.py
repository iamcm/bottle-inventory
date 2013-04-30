

from Crypto.Hash import SHA, MD5
import os
import datetime
import settings
from models import Logger
from models.BaseModel import BaseModel

class User(BaseModel):
    
    def __init__(self,_DBCON, _id=None, email=None, password=None):
        """
        Class to represent a user.
        
        There are two salts to every password, one is stored in settings.py 
        and never changes, the other comes from a generated random
        sequence and is stored in the database along with the password hash
        """
        self._salt = settings.SALT
        self.fields = [
            ('email', email),
            ('password', password),
            ('token', ''),
            ('salt', ''),
            ('valid', False),
            ('facebookuserId', None),
            ('added', datetime.datetime.now()),
        ]
        super(self.__class__, self).__init__(_DBCON, _id)
        
        if email and password:
            self.get_user()
    
    def get_password_hash(self, salt):
        h = SHA.new()
        h.update(self.password + self._salt + salt)
        return h.hexdigest()
        
    def generate_token(self):        
        h = MD5.new()
        h.update(os.urandom(20).decode('ascii', 'ignore'))
        return h.hexdigest()
    
    def save(self, newPassword=False):
        user = self.db.User.find_one({'email':self.email})
        
        if user is None or newPassword:
            self.salt = os.urandom(20).decode('ascii', 'ignore')
            self.password = self.get_password_hash(self.salt)
            self.token = self.generate_token()
        

        super(self.__class__, self).save()
    
    def activate(self, token):
        user = self.db.User.find_one({'token':token})
        
        if user:
            self._id = user['_id']
            user['token'] = ''
            user['valid'] = True
            
            self.db.User.save(user)
            super(self.__class__, self).__init__(self.db, user['_id'])

            return True
        else:
            return False
        
        
    def get_user(self):
                
        user = self.db.User.find_one({
            'email':self.email,
            'valid':True
        })
        
        if user:
            hash = self.get_password_hash(user.get('salt'))
            if user.get('password')== hash:
                super(self.__class__, self).__init__(self.db, user['_id'])
        