# -*- coding: utf-8 -*-
import rpyc
import sys
from .user import User
sys.path.append('..')

userList = { }
groupList = { }

class ServerService(rpyc.Service):
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
    @classmethod # this is an exposed method
    def createUser(cls): 
        pass
    @classmethod # this is an exposed method
    def createGroup(cls):
        pass
    @classmethod # this is an exposed method
    def deleteUser(cls):
        pass
    @classmethod # this is an exposed method
    def deleteGroup(cls):
        pass
    @classmethod # this is an exposed method
    def sendMessageUser(cls):
        pass
    @classmethod # this is an exposed method
    def sendMessageGroup(cls):
        pass

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ServerService, port=27000)
    t.start()
