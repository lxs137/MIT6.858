#!/usr/bin/python

import rpclib
import sys
from pcode import get_pcode, update_pcode
from debug import *

class PcodeRpcServer(rpclib.RpcServer):
    def rpc_get_pcode(self, username):
        return get_pcode(username)

    def rpc_update_pcode(self, username, token, pcode):
        return update_pcode(username, token, pcode)
    
(_, dummy_zookld_fd, sockpath) = sys.argv

s = PcodeRpcServer()
s.run_sockpath_fork(sockpath)
