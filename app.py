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
def index():
    collections = EntityManager(_DBCON).get_all(Collection
                            , filter_criteria={'userId':bottle.request.session.userId})

    output = []
    for c in collections:
        output.append( c.get_json_safe() )

    return json.dumps(output)

@bottle.route('/collection', method='POST') 
@checklogin
def index():
    id = bottle.request.json.get('id')
    name = bottle.request.json.get('name')
    items = bottle.request.json.get('items')
    
    c = Collection(_DBCON, id)
    c.name = name
    if items:
        for i in items:
            c.items.append(i)
    c.userId = bottle.request.session.userId
    c.save()

    return json.dumps({'result':True})


@bottle.route('/item/save', method='GET') 
@checklogin
def index():
    id = bottle.request.GET.get('id')
    name = bottle.request.GET.get('name')
    if bottle.request.GET.get('collectionIds'):
        collectionIds = bottle.request.GET.get('collectionIds').split(',')
    else:
        collectionIds = []

    i = Item(_DBCON, id)
    i.name = name
    i.userId = bottle.request.session.userId
    i.save()

    for id in collectionIds:
        c = Collection(_DBCON, _id=id)
        c.items.append(i._id)
        c.items = [i for i in set(c.items)]
        c.save()

    return json.dumps({'result':True})


@bottle.route('/items', method='GET') 
@checklogin
def index():
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
