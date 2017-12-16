# -*- coding: utf-8 -*-
import rpyc
import sys
sys.path.append('..')
import logging
from models.user import User
from models.group import Group
from validation import emailValidation

import controllers.friends as FriendController
import controllers.users as UserController


userList = { }
groupList = { }

class ServerService(rpyc.Service):
    userConected = None
    user = None
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
    def exposed_createUser(cls, name, email):
        # Validate
        validation = emailValidation(email)
        if(len(validation) > 0):
            logging.debug(validation)
            return validation
        # Persiste
        cls.user = User(name=name, email=email)
        cls.user.save()
        # Return
        data = {
            'type': '@USER/DATA',
            'payload': {
                'name': cls.user.getName(),
                'email': cls.user.getemail()
            }
        }
        logging.debug(data)
        return data
    @classmethod # this is an exposed method
    def exposed_createFriendship(cls, friend_email):
        friend = UserController.findBy_email(friend_email)
        if friend is None:
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Amigo nao encontrado! Verifique se o e-mail esta correto.'
            }
        FriendController.createFriendship(cls.user.getemail(), friend_email)
        return {
            'type': '@USER/DATA',
            'payload': FriendController.all(cls.user.getemail())
        }
    @classmethod # this is an exposed method
    def exposed_allFriends(cls):
        friendList = FriendController.all(cls.user.getemail())
        if len(friendList) is 0:
            return {
                'type': '@USER/ZERO',
                'payload': 'Sem amigos na lista!'
            }
        return {
            'type': '@USER/DATA',
            'payload': friendList
        }
    @classmethod # this is an exposed method
    def exposed_createGroup(cls, group):
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
    def exposed_findUserByEmail(cls, email):
        user = UserController.findBy_email(email)
        if user is None:
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Usuario não encontrado'
            }
        return {
            'type': '@USER/DATA',
            'payload': user
        }
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
        return UserController.all()
    @classmethod # this is an exposed method
    def exposed_allGroupsList(cls):
        return userList
    @classmethod # this is an exposed method
    def exposed_userLogin(cls, email):
        cls.user = UserController.findBy_email(email)
        if cls.user is None:
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Usuario não encontrado'
            }
        return {
            'type': '@USER/DATA',
            'payload': {
                'name': cls.user.getName(),
                'email': cls.user.getemail()
                }
        }
