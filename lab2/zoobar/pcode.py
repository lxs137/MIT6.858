from zoodb import *
from debug import *

import auth_client

def get_pcode(username):
    pcode_db = pcode_setup()
    pcode = pcode_db.query(Pcode).get(username)
    if not pcode or not pcode.profile:
        return ''
    code = pcode.profile.encode('ascii', 'ignore')
    code = code.replace('\r\n', '\n')
    return code

def update_pcode(username, token, pcode):
    if not auth_client.check_token(username, token):
        raise ValueError()       
    pcode_db = pcode_setup()
    pcode_item = pcode_db.query(Pcode).get(username)
    if not pcode_item:
        pcode_item = Pcode()
        pcode_item.username = username
        pcode_item.profile = pcode
        pcode_db.add(pcode_item)
    else:    
        pcode_item.profile = pcode
    pcode_db.commit()
