# -*- coding: utf-8 -*-
import rpyc
import sys
sys.path.append('..')
import logging
from models.user import User
from models.group import Group
from validation import loginValidation

from controllers.users import all as allUsers


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
    def exposed_createUser(cls, loginName):
        # Validate
        validation = loginValidation(loginName)
        if(len(validation) > 0):
            logging.debug(validation)
            return validation
        # Persiste
        newUser = User(loginName)
        newUser.save()
        # Return
        data = {
            'type': '@USER/DATA',
            'payload': newUser
        }
        logging.debug(data)
        return data
    @classmethod # this is an exposed method
    def exposed_createFriendship(cls, user, friend):
        # Validate
        validation = loginValidation(user)
        if(len(validation) > 0):
            logging.debug(validation)
            return validation
        # Persiste
        newUser = User(user)
        userList.setdefault(newUser.getId(), newUser)
        # Return
        data = {
            'type': '@USER/DATA',
            'payload': newUser
        }
        logging.debug(data)
        return data
    @classmethod # this is an exposed method
    def exposed_createGroup(cls, group):
        # Validate
        validation = loginValidation(group)
        if(len(validation) > 0):
            logging.debug(validation)
            return validation
        # Persiste
        newGroup = User(group)
        userList.setdefault(newGroup.getId(), newGroup)
        # Return
        data = {
            'type': '@USER/DATA',
            'payload': newGroup
        }
        logging.debug(data)
        return data
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
    # ALL
    #
    @classmethod # this is an exposed method
    def exposed_allUsers(cls):
        logging.info('Retornando lista de usuarios')
        return allUsers()
    @classmethod # this is an exposed method
    def exposed_allGroupsList(cls):
        return userList
