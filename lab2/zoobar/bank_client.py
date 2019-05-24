from zoodb import *
from debug import *

import time
import rpclib

sockpath = '/banksvc/sock'


def transfer(sender, recipient, zoobars, token):
    with rpclib.client_connect(sockpath) as c:
        return c.call('transfer', sender=sender, recipient=recipient, zoobars=zoobars, token=token)

def init(username):
    with rpclib.client_connect(sockpath) as c:
        return c.call('init', username=username)

def balance(username):
    with rpclib.client_connect(sockpath) as c:
        return c.call('balance', username=username)

def get_log(username):
    with rpclib.client_connect(sockpath) as c:
        return c.call('get_log', username=username)

