from zoodb import *
from debug import *

import hashlib
import random
import binascii
import os
import pbkdf2

SALT_LEN = 10

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == pbkdf2.PBKDF2(password, cred.salt).hexread(32):
        return newtoken(db, cred)
    else:
        return None

def get_user(username):
    db = person_setup()
    user_info = db.query(Person).get(username)
    if not user_info:
        return None
    return user_info.as_dict()

def register(username, password):
    db = cred_setup()
    if db.query(Cred).get(username):
        return None
    newcred = Cred()
    newcred.username = username
    salt = binascii.hexlify(os.urandom(SALT_LEN)).decode()
    newcred.password = pbkdf2.PBKDF2(password, salt).hexread(32)
    newcred.salt = salt
    db.add(newcred)
    return newtoken(db, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

