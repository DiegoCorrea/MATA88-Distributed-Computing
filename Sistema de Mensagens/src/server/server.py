# -*- coding: utf-8 -*-
import rpyc
import sys, re, operator
sys.path.append('..')
import logging

import controllers.chats as ChatController
import controllers.users as UserController
import controllers.groups as GroupController
import controllers.contacts as ContactController

class ServerService(rpyc.Service):
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
    # # # # # # # # # # # #
    # USER Interface      #
    # # # # # # # # # # # #
    @classmethod # this is an exposed method
    def exposed_createUser(cls, name, email):
        logging.info('Start [Create User]')
        # Validate
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
            logging.info('Finish [Create User] - return: @VALIDATION/ERROR')
            return {
                'type': '@VALIDATION/NOT_EMAIL',
                'payload': { }
            }
        if len(name) == 0:
            logging.info('Finish [Create User] - return: @VALIDATION/SMALL_NAME')
            return {
                'type': '@VALIDATION/SMALL_NAME',
                'payload': { }
            }
        if len(UserController.findBy_email(email)) != 0:
            logging.info('Finish [Create User] - return: @VALIDATION/EXISTENT')
            return {
                'type': '@VALIDATION/EXISTENT',
                'payload': { }
            }
        # Persiste
        UserController.create(email=email, name=name)
        user = UserController.findBy_email(email=email)
        # Return
        logging.info('Finish [Create User] - return: @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'email': user[0],
                'name': user[1]
            }
        }
    @classmethod # this is an exposed method
    def exposed_findUserByEmail(cls, email):
        logging.info('Start [FIND USER BY EMAIL]')
        user = UserController.findBy_email(email)
        if len(user) == 0:
            logging.info('Finish [FIND USER BY EMAIL] - return @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': { }
            }
        logging.info('Finish [FIND USER BY EMAIL] - return @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'email': user[0],
                'name': user[1]
            }
        }
    @classmethod # this is an exposed method
    def exposed_userLogin(cls, user_id):
        logging.info('Start [User Login]')
        user = UserController.findBy_email(user_id)
        if len(user) == 0:
            logging.info('Finish [User Login] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': { }
            }
        chatList = cls.exposed_allChats(user_id)
        userGroups = cls.exposed_userAllGroups(user_id)
        logging.info('Finish [User Login] - return: @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'user': {
                    'email': user[0],
                    'name': user[1]
                },
                'friendships': { },
                'chats': chatList['payload'],
                'groups': userGroups['payload']
            }
        }
    # # # # # # # # # # # #
    # USER CHAT Interface #
    # # # # # # # # # # # #
    @classmethod # this is an exposed method
    def exposed_createChat(cls, user_id, friend_id):
        logging.info('Start [Create Chat]')
        user = UserController.findBy_ID(user_id)
        friend = UserController.findBy_ID(friend_id)
        if len(friend) == 0 or len(user) == 0:
            logging.info('Finish [Create Chat] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': { }
            }
        if len(ChatController.getChatWith(user_id=user_id, friend_id=friend_id)) == 0:
            ChatController.createChat(user_id=user_id, friend_id=friend_id)
        logging.info('Finish [Create Chat] - return: cls.exposed_allChats(user_id)')
        return cls.exposed_allChats(user_id)
    @classmethod # this is an exposed method
    def exposed_allChats(cls, user_id):
        logging.info('Start [All Chat]')
        userChatList = {}
        for chat in ChatController.allUserChat(user_id=user_id):
            if chat[1] == user_id:
                userChatList.setdefault(chat[2], {
                    'chatWith': chat[2],
                    'created_at': chat[3],
                    'messages': { }
                })
            else:
                userChatList.setdefault(chat[1], {
                    'chatWith': chat[1],
                    'created_at': chat[3] ,
                    'messages': { }
                })
        if len(userChatList) == 0:
            logging.info('Finish [All Chat] - return: @CHAT/ZERO')
            return {
                'type': '@CHAT/ZERO',
                'payload': { }
            }
        logging.info('Finish [All Chat] - return: @CHAT/DATA')
        return {
            'type': '@CHAT/DATA',
            'payload': userChatList
        }
    @classmethod # this is an exposed method
    def exposed_chatMessageHistory(cls, user_id, friend_id):
        logging.info('Start [CHAT MESSAGE HISTORY]')
        chatMessageHistory = {}
        chat = ChatController.getChatWith(user_id, friend_id)
        if len(chat) == 0:
            logging.info('Finish [CHAT MESSAGE HISTORY] - return: @CHAT/NOTFOUND')
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
            logging.info('Finish [CHAT MESSAGE HISTORY] - return: @CHAT/MESSAGE/ZERO')
            return {
                'type': '@CHAT/MESSAGE/ZERO',
                'payload': { }
            }
        logging.info('Finish [CHAT MESSAGE HISTORY] - return: @CHAT/MESSAGE/DATA')
        return {
            'type': '@CHAT/MESSAGE/DATA',
            'payload': chatMessageHistory
        }
    @classmethod # this is an exposed method
    def exposed_sendMessageUser(cls, user_id, friend_id, message):
        logging.info('Start [SEND MESSAGE USER]')
        chat = ChatController.getChatWith(user_id=user_id, friend_id=friend_id)
        if len(chat) == 0:
            ChatController.createChat(user_id=user_id, friend_id=friend_id)
            chat = ChatController.getChatWith(user_id=user_id, friend_id=friend_id)
            if len(chat) == 0:
                logging.info('Finish [CHAT MESSAGE HISTORY] - return: @CHAT/NOTFOUND')
                return {
                    'type': '@CHAT/NOTFOUND',
                    'payload': { }
                }
        ChatController.setChatMessage(chat_id=chat[0], sender_id=user_id, message=message)
        logging.info('Finish [SEND MESSAGE USER] - return: cls.exposed_chatMessageHistory(user_id, friend_id)')
        return cls.exposed_chatMessageHistory(user_id, friend_id)
    # # # # # # # # # #
    # GROUP Interface #
    # # # # # # # # # #
    @classmethod # this is an exposed method
    def exposed_createGroup(cls, user_id, group_name):
        logging.info('Start [CREATE GROUP]')
        if len(group_name) == 0:
            logging.info('Finish [CREATE GROUP] - return: @VALIDATION/SMALL_NAME')
            return {
                'type': '@VALIDATION/SMALL_NAME',
                'payload': { }
            }
        group_id = GroupController.createGroup(group_name)
        if len(group_id) == 0:
            logging.info('Finish [CREATE GROUP] - return: @GROUP/ZERO')
            return {
                'type': '@GROUP/ZERO',
                'payload': { }
            }
        GroupController.addUser(user_id, group_id)
        logging.info('Finish [CREATE GROUP] - return: cls.exposed_userAllGroups(user_id)')
        return cls.exposed_userAllGroups(user_id)
    @classmethod # this is an exposed method
    def exposed_userAllGroups(cls, user_id):
        logging.info('Start [User All Groups]')
        groupList = GroupController.userGroups(user_id=user_id)
        if len(groupList) == 0:
            logging.info('Finish [User All Groups] - return: @GROUP/ZERO')
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
        logging.info('Finish [User All Groups] - return: @GROUP/DATA')
        return {
            'type': '@GROUP/DATA',
            'payload': groupData
        }
    @classmethod # this is an exposed method
    def exposed_addUserToGroup(cls, user_id, group_id):
        logging.info('Start [Add User To a Group]')
        if len(GroupController.findBy_ID(group_id=group_id)) == 0:
            logging.info('Finish [Add User To a Group] - return: @GROUP/NOTFOUND')
            return {
                'type': '@GROUP/NOTFOUND',
                'payload': { }
            }
        GroupController.addUser(user_id, group_id)
        logging.info('Finish [Add User To a Group] - return: cls.exposed_userAllGroups(user_id)')
        return cls.exposed_userAllGroups(user_id)
    # # # # # # # # # # # #
    # CONTACT Interface   #
    # # # # # # # # # # # #
    @classmethod # this is an exposed method
    def exposed_addContact(cls, user_id, contact_id):
        logging.info('Start [Add Contact]')
        contact = ContactController.findBy_ID(user_id=user_id, contact_id=contact_id)
        if len(contact) == 0:
            logging.info('Finish [Add Contact] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': { }
            }
        ContactController.create(user_id=user_id, contact_id=contact_id)
        logging.info('Finish [Add Contact] - return: cls.exposed_allUserContacts(user_id)')
        return cls.exposed_allUserContacts(user_id)
    @classmethod # this is an exposed method
    def exposed_allUserContacts(cls, user_id):
        user = UserController.findBy_email(user_id)
        if len(user) == 0:
            logging.info('Finish [User All Groups] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': { }
            }
        contacts = ContactController.all(user_id=user_id)
        if len(contacts) == 0:
            logging.info('Finish [User All Groups] - return: @@@@@@@@@@@@@@@')
            return {
                'type': '@@@@@@@@@@@@@',
                'payload': { }
            }
        userContactList = { }
        for contact in contacts:
            groupData.setdefault(contact[2], {
                'contact_id': contact[2],
                'name': '!!!!!!!!!!!!!!!!!',
                'created_at': contact[3],
            })
        logging.info('Finish [User All Groups] - return: @GROUP/DATA')
        return {
            'type': '@GROUP/DATA',
            'payload': groupData
        }
