# -*- coding: utf-8 -*-
import rpyc
import sys
import operator
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
        user = User(name=name, email=email)
        user.save()
        # Return
        data = {
            'type': '@USER/DATA',
            'payload': {
                'name': user.getName(),
                'email': user.getemail()
            }
        }
        logging.debug(data)
        return data
    @classmethod # this is an exposed method
    def exposed_createChat(cls, user_id, friend_id):
        friend = UserController.findBy_id(friend_id)
        if friend is None:
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Amigo nao encontrado! Verifique se o e-mail esta correto.'
            }
        if len(ChatController.getChatWith(user_id=user_id, friend_id=friend_id)) == 0:
            ChatController.createChat(user_id=user_id, friend_id=friend_id)
        return cls.exposed_allChats(user_id)
    @classmethod # this is an exposed method
    def exposed_allChats(cls, user_id):
        chatList = {}
        for chat in ChatController.allUserChat(user_id=user_id):
            if chat[1] == user_id:
                chatList.setdefault(chat[2], {'chatWith': chat[2], 'created_at': chat[3]})
            else:
                chatList.setdefault(chat[1], {'chatWith': chat[1], 'created_at': chat[3]})
        if len(chatList) == 0:
            return {
                'type': '@CHAT/ZERO',
                'payload': { }
            }
        return {
            'type': '@CHAT/DATA',
            'payload': chatList
        }
    @classmethod # this is an exposed method
    def exposed_chatMessageHistory(cls, user_id, friend_id):
        chatMessageHistory = {}
        chat = ChatController.getChatWith(user_id, friend_id)
        if len(chat) == 0:
            return {
                'type': '@CHAT/NOTFOUND',
                'payload': { }
            }
        for chat_message in ChatController.getChatMessages(chat[0]):
            chatMessageHistory.setdefault(chat_message[4], {
                'chat_id': chat_message[1],
                'sender_id': chat_message[2],
                'message': chat_message[3],
                'created_at': chat_message[4]
            })
        if len(chatMessageHistory) == 0:
            return {
                'type': '@CHAT/ZERO',
                'payload': { }
            }
        return {
            'type': '@CHAT/DATA',
            'payload': chatMessageHistory
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
    def exposed_sendMessageUser(cls, user_id, friend_id, message):
        chat = ChatController.getChatWith(user_id=user_id, friend_id=friend_id)
        if len(chat) == 0:
            ChatController.createChat(user_id=user_id, friend_id=friend_id)
            chat = ChatController.getChatWith(user_id=user_id, friend_id=friend_id)
            if len(chat) == 0:
                return {
                    'type': '@USER/NOTFOUND',
                    'payload': 'Amigo nao encontrado! Verifique se o e-mail esta correto.'
                }
        ChatController.setChatMessage(chat_id=chat[0], sender_id=user_id, message=message)
        return cls.exposed_chatMessageHistory(user_id, friend_id)
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
    @classmethod # this is an exposed method
    def exposed_userLogin(cls, user_id):
        user = UserController.findBy_email(user_id)
        if user is None:
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Usuario não encontrado'
            }
        return {
            'type': '@USER/DATA',
            'payload': {
                'name': user.getName(),
                'email': user.getemail()
                }
        }
