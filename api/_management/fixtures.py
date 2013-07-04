import os, sys
sys.path.append(os.path.abspath( os.path.join(__file__,'../..')))

from db import _DBCON
from models.EntityManager import EntityManager
from dateutil import parser
"""
from models.User import User

u = User(_DBCON)
u.email = 'i.am.chrismitchell@gmail.com'
u.password = 'pass'
u.valid= True
u.save(True)

"""