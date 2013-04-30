import bottle

import settings
from db import _DBCON
from controllers.BaseController import BaseController
from models.User import User
from models.Session import Session
from models.Email import Email
from models import Logger

def checklogin(callback):
    def wrapper(*args, **kwargs):
        if bottle.request.get_cookie('token') or bottle.request.GET.get('token'):
            token = bottle.request.get_cookie('token') or bottle.request.GET.get('token')
            
            s = Session(_DBCON, publicId=token)
            if not s.valid or not s.check(bottle.request.get('REMOTE_ADDR'), bottle.request.get('HTTP_USER_AGENT')):
                return bottle.HTTPError(403, 'Access denied')
                
            else:
                bottle.request.session = s
                return callback(*args, **kwargs)
        else:
            return bottle.HTTPError(403, 'Access denied')
    return wrapper


class AuthController(BaseController):

    def _login_user(self, u):
        s = Session(_DBCON)
        s.userId = u._id
        s.ip = bottle.request.get('REMOTE_ADDR')
        s.userAgent = bottle.request.get('HTTP_USER_AGENT')
        s.save()

        return s
    
    
    def login(self, e, p):

        if e and p:
            u = User(_DBCON, email=e, password=p)
            u.activate('76e8f1cbbf8007c490d2abf6b82d9064')
            Logger.log_to_file(u.get_json())    

            if u._id and u.valid:
                s = self._login_user(u)
                return s.publicId

        return bottle.HTTPError(403, 'Access denied')


    @checklogin
    def logout(self):
        s = bottle.request.session
        s.destroy()
        
        return bottle.redirect('/login')
    

