from debug import *
from zoodb import *
import rpclib

sockpath = '/pcodesvc/sock'

def get_pcode(username):
    with rpclib.client_connect(sockpath) as c:
        return c.call('get_pcode', username=username)

def update_pcode(username, token, pcode):
	with rpclib.client_connect(sockpath) as c:
		return c.call('update_pcode', username=username, token=token, pcode=pcode)
