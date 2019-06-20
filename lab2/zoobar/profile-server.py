#!/usr/bin/python

import rpclib
import sys
import os
import base64
import sandboxlib
import urllib
import hashlib
import socket
import bank_client
import auth_client
import pcode_client
import zoodb

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor):
        self.user = user
        self.visitor = visitor
        # get self token
        cred_db = zoodb.cred_setup()
        self_cred = cred_db.query(zoodb.Cred).get(self.user)
        if not self_cred:
            return None
        self.token = self_cred.token
        # switch uid
        os.setresuid(61016, 61016, 61016)

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank_client.get_log(username):
            print "%s: %s" % (username, xfer)
            xfers.append({ 'sender': xfer['sender'],
                           'recipient': xfer['recipient'],
                           'amount': xfer['amount'],
                           'time': xfer['time'],
                         })
        return xfers

    def rpc_get_user_info(self, username):
        return { 'username': username,
                 'zoobars': bank_client.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank_client.transfer(self.user, target, zoobars, self.token)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, user, visitor):
        uid = 61017

        userdir = '/tmp/%s' % base64.b64encode(user.encode('utf-8'))
        if not os.path.exists(userdir):
            os.mkdir(userdir, 0700)
            os.chown(userdir, uid, uid)

        pcode = pcode_client.get_pcode(user)

        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
