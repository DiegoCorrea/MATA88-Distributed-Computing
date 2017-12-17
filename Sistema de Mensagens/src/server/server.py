# -*- coding: utf-8 -*-
import rpyc
import sys
sys.path.append('..')
import logging
from models.user import User
from models.group import Group
from validation import emailValidation

import controllers.chats as ChatController
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
    def exposed_createChat(cls, friend_id):
        friend = UserController.findBy_id(friend_id)
        if friend is None:
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Amigo nao encontrado! Verifique se o e-mail esta correto.'
            }
        ChatController.createChat(user_id=cls.user.getID(), friend_id=friend_id)
        chatList = {}
        for friend in ChatController.all(user_id=cls.user.getID()):
            chatList.setdefault(friend[0], {'friendOf': friend[0], 'created_at': friend[1]})
        return {
            'type': '@USER/DATA',
            'payload': chatList
        }
    @classmethod # this is an exposed method
    def exposed_allFriends(cls):
        chatList = {}
        for friend in ChatController.all(user_id=cls.user.getID()):
            chatList.setdefault(friend[0], {'friendOf': friend[0], 'created_at': friend[1]})
        if len(chatList) is 0:
            return {
                'type': '@USER/ZERO',
                'payload': 'Sem amigos na lista!'
            }
        return {
            'type': '@USER/DATA',
            'payload': chatList
        }
    @classmethod # this is an exposed method
    def exposed_chatHistory(cls, friend_id):
        chatHistory = ChatController.getChatHistory(cls.user.getID(), friend_id)
        if len(chatHistory) is 0:
            return {
                'type': '@CHAT/ZERO',
                'payload': 'Sem conversas no chat!'
            }
        return {
            'type': '@CHAT/DATA',
            'payload': chatHistory
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
    def exposed_sendMessageUser(cls, friend_id, message):
        chat = ChatController.getChatWith(user_id=cls.user.getID(), friend_id=friend_id)
        if len(chat) is 0:
            ChatController.createChat(user_id=cls.user.getID(), friend_id=friend_id)
            chat = ChatController.getChatWith(user_id=cls.user.getID(), friend_id=friend_id)
            if len(chat) is 0:
                return {
                    'type': '@USER/NOTFOUND',
                    'payload': 'Amigo nao encontrado! Verifique se o e-mail esta correto.'
                }
        ChatController.setChatMessage(chat_id=chat[0], sender_id=cls.user.getID(), message=message)
        chatHistory = {}
        for chat_message in ChatController.getChatHistory(cls.user.getID(), friend_id):
            chatHistory.setdefault(chat_message[4], {
                'chat_id': chat_message[1],
                'sender_id': chat_message[2],
                'message': chat_message[3],
                'created_at': chat_message[4]
            })
        return {
            'type': '@CHAT/DATA',
            'payload': chatHistory
        }
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
    def exposed_userLogin(cls, user_id):
        cls.user = UserController.findBy_email(user_id)
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
