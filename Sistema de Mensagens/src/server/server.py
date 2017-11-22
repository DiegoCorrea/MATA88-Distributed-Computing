# -*- coding: utf-8 -*-
import rpyc
import sys
sys.path.append('..')
from user import User

userList = { }
groupList = { }

class ServerService(rpyc.Service):
    userConected = None
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
    #
    # CREATORS
    #
    @classmethod # this is an exposed method
    def createUser(cls, name): 
        newUser = User(name)
        userList.setdefault(newUser.getId(), newUser)
        return newUser
    @classmethod # this is an exposed method
    def createGroup(cls, name):
        pass
    #
    # REMOVERS
    #
    @classmethod # this is an exposed method
    def deleteUser(cls, id):
        pass
    @classmethod # this is an exposed method
    def deleteGroup(cls, id):
        pass
    #
    # SENDERS
    #
    @classmethod # this is an exposed method
    def sendMessageUser(cls, id, message):
        pass
    @classmethod # this is an exposed method
    def sendMessageGroup(cls, id, message):
        pass
    #
    # FINDERS
    #
    @classmethod # this is an exposed method
    def findUserByName(cls, name):
        pass
    @classmethod # this is an exposed method
    def findGroupByName(cls, name):
        pass
    @classmethod # this is an exposed method
    def findUserById(cls, id):
        pass
    @classmethod # this is an exposed method
    def findGroupById(cls, id):
        pass
    #
    # ALL
    #
    @classmethod # this is an exposed method
    def allGroupList(cls, id):
        pass
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ServerService, port=27000)
    t.start()
