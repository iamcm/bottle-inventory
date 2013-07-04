import os, sys
sys.path.append(os.path.abspath( os.path.join(__file__,'../..')))

from bson import ObjectId
from db import _DBCON
from models.EntityManager import EntityManager
from models.User import User
from models.Models import *

u = EntityManager(_DBCON).get_all(User)[0]

print(u.password)
