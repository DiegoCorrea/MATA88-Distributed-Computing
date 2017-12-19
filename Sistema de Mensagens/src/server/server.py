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
import controllers.groups as GroupController


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
        logging.info('Start Create User')
        # Validate
        if(len(email) <= 3):
            logging.info('Finish Create User - return: VALIDATION/ERROR')
            return {
                'type': 'VALIDATION/ERROR',
                'payload': 'Nome de usuario menor do que o requisitado! O minimo requisitado eh 3.'
            }
        if(UserController.findBy_email(email) != None):
            logging.info('Finish Create User - return: VALIDATION/ERROR')
            return {
                'type': 'VALIDATION/ERROR',
                'payload': 'Usuario ja cadastrado!'
            }
        # Persiste
        user = User(name=name, email=email)
        user.save()
        # Return
        logging.info('Finish Create User - return: @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'name': user.getName(),
                'email': user.getemail()
            }
        }
    @classmethod # this is an exposed method
    def exposed_createChat(cls, user_id, friend_id):
        logging.info('Start Create Chat')
        friend = UserController.findBy_id(friend_id)
        if friend is None:
            logging.info('Finish Create Chat - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Amigo nao encontrado! Verifique se o e-mail esta correto.'
            }
        if len(ChatController.getChatWith(user_id=user_id, friend_id=friend_id)) == 0:
            ChatController.createChat(user_id=user_id, friend_id=friend_id)
        logging.info('Finish Create Chat - return: cls.exposed_allChats(user_id)')
        return cls.exposed_allChats(user_id)
    @classmethod # this is an exposed method
    def exposed_allChats(cls, user_id):
        logging.info('Start All Chat')
        chatList = {}
        for chat in ChatController.allUserChat(user_id=user_id):
            if chat[1] == user_id:
                chatList.setdefault(chat[2], {'chatWith': chat[2], 'created_at': chat[3], 'messages': { }})
            else:
                chatList.setdefault(chat[1], {'chatWith': chat[1], 'created_at': chat[3] , 'messages': { }})
        if len(chatList) == 0:
            logging.info('Finish All Chat - return: @CHAT/ZERO')
            return {
                'type': '@CHAT/ZERO',
                'payload': { }
            }
        logging.info('Finish All Chat - return: @CHAT/DATA')
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
    def exposed_createGroup(cls, user_id, group_name):
        group_id = GroupController.createGroup(group_name)
        if len(group_id) == 0:
            return {
                'type': '@GROUP/ZERO',
                'payload': { }
            }
        GroupController.addUser(user_id, group_id)
        return cls.exposed_userAllGroups(user_id)
    @classmethod # this is an exposed method
    def exposed_userAllGroups(cls, user_id):
        logging.info('Start User All Groups')
        groupList = GroupController.userGroups(user_id=user_id)
        if len(groupList) == 0:
            logging.info('Finish User All Groups - return: @GROUP/ZERO')
            return {
                'type': '@GROUP/ZERO',
                'payload': { }
            }
        groupData = { }
        for userGroup in groupList:
            group = GroupController.findBy_ID(userGroup[2])
            groupData.setdefault(userGroup[2], {
                'group_id': userGroup[2],
                'name': group[1],
                'join_at': userGroup[3],
                'created_at': group[2],
                'messages': { }
            })
        logging.info('Finish User All Groups - return: @GROUP/DATA')
        return {
            'type': '@GROUP/DATA',
            'payload': groupData
        }
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
        logging.info('Start User Login')
        user = UserController.findBy_email(user_id)
        chatList = {}
        for chat in ChatController.allUserChat(user_id=user_id):
            if chat[1] == user_id:
                chatList.setdefault(chat[2], {'chatWith': chat[2], 'created_at': chat[3]})
            else:
                chatList.setdefault(chat[1], {'chatWith': chat[1], 'created_at': chat[3]})
        if user is None:
            logging.info('Finish User Login - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': 'Usuario não encontrado'
            }
        logging.info('Finish User Login - return: @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'user': {
                    'name': user.getName(),
                    'email': user.getemail()
                },
                'friendships': { },
                'chats': chatList,
                'groups': { }
            }
        }
