import datetime
import json
import random
import bottle

import db
from db import _DBCON
from models import Logger
from models.EntityManager import EntityManager
from models import Util
import settings
from controllers.BaseController import BaseController
from controllers.AuthController import checklogin
from models.User import User
from models.Collection import Collection
from models.Item import Item

class DefaultController(BaseController):
    
    def __init__(self):
        bottle.response.content_type = 'application/json'
        

    @checklogin
    def saveCollection(self, name, id=None, items=[]):
        c = Collection(_DBCON, id)
        c.name = name
        for i in items:
            c.items.append(i)
        c.userId = bottle.request.session.userId
        c.save()

        return json.dumps({'result':True})

            
    @checklogin
    def getCollections(self):
        collections = EntityManager(_DBCON).get_all(Collection
                                , filter_criteria={'userId':bottle.request.session.userId})

        output = []
        for c in collections:
            output.append( c.get_json_safe() )

        return json.dumps(output)


    @checklogin
    def saveItem(self, name, id=None, collectionIds=[]):
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

            
    @checklogin
    def getItems(self, collectionId=None):
        if collectionId:
            collections = EntityManager(_DBCON).get_all(Item
                                , filter_criteria={
                                    'userId':bottle.request.session.userId,
                                    'collections':{
                                        '$in':[collectionId]
                                    }
                                })
        else:
            collections = EntityManager(_DBCON).get_all(Item
                                , filter_criteria={'userId':bottle.request.session.userId})

        output = []
        for c in collections:
            output.append( c.get_json_safe() )

        return json.dumps(output)


    def favicon(self):

        return "Shaka"
        
