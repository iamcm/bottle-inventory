import bottle
from bottle import route
from controllers.DefaultController import DefaultController
from controllers.AuthController import AuthController
import settings

########## AUTH ##############
@route('/login')
def index():
    e = bottle.request.GET.get('email')
    p = bottle.request.GET.get('password')
    return AuthController().login(e, p)

@route('/logout', method='GET')
def index():
    return AuthController().logout()

"""
@route('/register', method='GET')
def index():
    return AuthController().register()

@route('/register', method='POST')
def index():
    return AuthController().register_post()

@route('/success', method='GET')
def index():
    return AuthController().register_success()

@route('/activate/<token>')
def index(token):
    return AuthController().activate_token(token)
"""
##############################



##############################
###### MAIN APP ROUTES #######
##############################
@route('/', method='GET') 
def index():
    return DefaultController().index()

@route('/favicon.ico', method='GET') 
def index():
    return DefaultController().favicon()

@route('/collections', method='GET') 
def index():
    return DefaultController().getCollections()

@route('/collection/save', method='GET') 
def index():
    id = bottle.request.GET.get('id')
    name = bottle.request.GET.get('name')
    return DefaultController().saveCollection(id=id, name=name)

@route('/item/save', method='GET') 
def index():
    id = bottle.request.GET.get('id')
    name = bottle.request.GET.get('name')
    if bottle.request.GET.get('collectionIds'):
        collectionIds = bottle.request.GET.get('collectionIds').split(',')
    else:
        collectionIds = []

    return DefaultController().saveItem(id=id, name=name, collectionIds=collectionIds)



@route('/login', method='POST') 
def index():
    e = bottle.request.POST.get('email')
    p = bottle.request.POST.get('password')

    return AuthController().login(e, p)


