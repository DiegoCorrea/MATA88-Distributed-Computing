# -*- coding: utf-8 -*-
import rpyc
import sys
sys.path.append('..')
from user import User
import logging

userList = []
groupList = []

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
    def exposed_createUser(cls, loginName):
        logging.info('[createUser] Start')
        newUser = User(loginName)
        userList.append(newUser)
        response = {
            'type': '@USER/CREATED', 
            'payload': {
                'id': str(newUser.getId()), 
                'name': str(newUser.getName())
            }
        }
        logging.info('[createUser] Response: ' + str(response))
        logging.info('[createUser] End')
        return response
    @classmethod # this is an exposed method
    def exposed_createGroup(cls, name):
        pass
    #
    # REMOVERS
    #
    @classmethod # this is an exposed method
    def exposed_deleteUser(cls, id):
        pass
    @classmethod # this is an exposed method
    def exposed_deleteGroup(cls, id):
        pass
    #
    # SENDERS
    #
    @classmethod # this is an exposed method
    def exposed_sendMessageUser(cls, id, message):
        pass
    @classmethod # this is an exposed method
    def exposed_sendMessageGroup(cls, id, message):
        pass
    #
    # FINDERS
    #
    @classmethod # this is an exposed method
    def exposed_findUserByName(cls, name):
        return {'type': '@USER/DATA', 'payload': 'payload'}
    @classmethod # this is an exposed method
    def exposed_findGroupByName(cls, name):
        pass
    @classmethod # this is an exposed method
    def exposed_findUserById(cls, id):
        pass
    @classmethod # this is an exposed method
    def exposed_findGroupById(cls, id):
        pass
    #
    # ALL FRIENDS
    #
    @classmethod # this is an exposed method
    def exposed_allUsersFriends(cls):
        logging.info('[allUsersFriends] Inicio')
        allUsers = []
        for user in userList:
            newUser = {
            'id': str(user.getId()),
            'name': str(user.getName())
            }
            allUsers.append(newUser)
        response = {
            'type': '@USER/FRIENDS', 
            'payload': allUsers
        }
        logging.info('[allUsersFriends] Response: ' + str(response))
        logging.info('[allUsersFriends] Fim ')
        return response
    @classmethod # this is an exposed method
    def exposed_allGroupsList(cls):
        return userList
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    logging.basicConfig(filename='server.log', filemode='w',level=logging.DEBUG)
    t = ThreadedServer(ServerService, port=27000)
    t.start()
