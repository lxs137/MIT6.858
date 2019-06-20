from flask import g
from debug import *

import rpclib
import traceback

def run_profile(username):
    try:
        with rpclib.client_connect('/profilesvc/sock') as c:
            return c.call('run', user=username,
                                 visitor=g.user.person.username)
    except Exception, e:
        traceback.print_exc()
        return 'Exception: ' + str(e)
