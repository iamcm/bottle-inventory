import random
import json
import datetime
import os 
import bottle
import settings
from db import _DBCON
from models import Util
from models.EntityManager import EntityManager
from models.User import User
from models.Session import Session
from models.Email import Email
from models.Collection import Collection
from models.Item import Item
from models.File import File
from models import Logger


# CONFIG
APPLICATIONROOT = os.path.dirname( os.path.abspath(__file__) )
USERFILES = APPLICATIONROOT + '/userfiles'

def randomfilename():
   return str( random.randint(1000, 1000000) ) 

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


def JSONResponse(callback):
    def wrapper(*args, **kwargs):
        bottle.response.content_type = 'text/json'
        return callback(*args, **kwargs)
    return wrapper


# static files
if settings.PROVIDE_STATIC_FILES:
    @bottle.route('/frontend/<filepath:path>')
    def index(filepath):
        return bottle.static_file(filepath, root=settings.ROOTPATH +'/frontend/')




# auth
@bottle.route('/login')
def index():
    e = bottle.request.GET.get('email')
    p = bottle.request.GET.get('password')

    if e and p:
        u = User(_DBCON, email=e, password=p)

        if u._id and u.valid:
            s = Session(_DBCON)
            s.userId = u._id
            s.ip = bottle.request.get('REMOTE_ADDR')
            s.userAgent = bottle.request.get('HTTP_USER_AGENT')
            s.save()

            return s.publicId

    return bottle.HTTPError(403, 'Access denied')


@bottle.route('/logout', method='GET')
@checklogin
def index():
    s = bottle.request.session
    s.destroy()
    
    return bottle.redirect('/login')




# main app routes
@bottle.route('/collections', method='GET') 
@checklogin
@JSONResponse
def index():
    collections = EntityManager(_DBCON).get_all(Collection
                            , filter_criteria={'userId':bottle.request.session.userId}
                            ,sort_by=[('lowercasename', 1)]
                            )

    output = []
    for c in collections:
        output.append( c.get_json_safe() )

    return json.dumps(output)


@bottle.route('/collection', method='POST') 
@checklogin
@JSONResponse
def index():
    id = bottle.request.POST.get('id')
    name = bottle.request.POST.get('name')
    
    c = Collection(_DBCON, id)
    c.name = name
    c.userId = bottle.request.session.userId
    c.save()

    return json.dumps({'result':True})


@bottle.route('/upload', method='POST')
@checklogin
def index():
    uploadedFile = bottle.request.files.get('file')
    nicename, ext = os.path.splitext(uploadedFile.filename)

    savepath = os.path.join(USERFILES, str(bottle.request.session.userId))

    if not os.path.isdir(savepath):
        os.mkdir(savepath)

    fullpath = os.path.join(savepath, randomfilename() + ext)
    while os.path.isfile(fullpath):
        fullpath = os.path.join(savepath, randomfilename() + ext)

    uploadedFile.save(fullpath)

    f = File(_DBCON)
    f.nicename = uploadedFile.filename
    f.sysname = os.path.split(fullpath)[1]
    f.sessionId = bottle.request.session.publicId
    f.userId = bottle.request.session.userId
    f.save()


@bottle.route('/item', method='POST') 
@checklogin
@JSONResponse
def index():
    id = bottle.request.POST.get('id')
    name = bottle.request.POST.get('name')
    if bottle.request.POST.get('collectionIds[]'):
        collectionIds = bottle.request.POST.get('collectionIds[]').split(',')
    else:
        collectionIds = []

    i = Item(_DBCON, id)
    i.name = name
    i.userId = bottle.request.session.userId

    for id in collectionIds:
        i.collections.append(id)
        i.collections = [c for c in set(i.collections)]
    
    #associate any previously uploaded files
    for f in EntityManager(_DBCON).get_all(File
                                , filter_criteria={
                                    'userId':bottle.request.session.userId,
                                    'sessionId':bottle.request.session.publicId
                                    }):
        i.files.append(f._id)
        f.sessionId = ''
        f.save()

    i.save()


    return json.dumps({'result':True})


@bottle.route('/items', method='GET') 
@checklogin
@JSONResponse
def index():
    collectionId = bottle.request.GET.get('collectionId')

    if collectionId:
        items = EntityManager(_DBCON).get_all(Item
                            , filter_criteria={
                                'userId':bottle.request.session.userId,
                                'collections':{
                                    '$in':[collectionId]
                                }
                            })
    else:
        items = EntityManager(_DBCON).get_all(Item
                            , filter_criteria={'userId':bottle.request.session.userId})

    output = []
    for i in items:
        output.append( i.get_json_safe() )

    return json.dumps(output)








#######################################################

if __name__ == '__main__':
    with open(settings.ROOTPATH +'/app.pid','w') as f:
        f.write(str(os.getpid()))

    if settings.DEBUG: 
        bottle.debug() 
        
    bottle.run(server=settings.SERVER, reloader=settings.DEBUG, host=settings.APPHOST, port=settings.APPPORT, quiet=(settings.DEBUG==False) )
