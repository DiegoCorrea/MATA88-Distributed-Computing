# -*- coding: utf-8 -*-
import sys, os
from time import sleep
import rpyc
import re
import socket, errno
SERVER_IP = 'localhost'
SERVER_PORT = 27000
SERVERCONNECTION = None
STORE = {
    'user': { },
    'contacts': { },
    'chats': { },
    'groups': { }
}
CONFIG = {
    'connected': False
}
################################################################################
################################################################################
################################################################################
def readGroupIDFromKey():
    inText = ''
    while inText == '':
        try:
            inText = raw_input("Group Code: ")
        except KeyboardInterrupt:
            exitProgram()
        except (NameError, SyntaxError):
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Wrong Input, try again!'
            inText = ''
    return inText
def readNameFromKey():
    inText = ''
    while inText == '':
        try:
            inText = raw_input("Name: ")
        except KeyboardInterrupt:
            exitProgram()
        except (NameError, SyntaxError):
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Wrong Input, try again!'
            inText = ''
    return inText
def readEmailFromKey():
    inText = ''
    while inText == '':
        try:
            inText = raw_input("Email: ")
        except KeyboardInterrupt:
            exitProgram()
        except (NameError, SyntaxError):
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Wrong Input, try again!'
            inText = ''
        if re.match(r"[^@]+@[^@]+\.[^@]+", inText) == None:
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Please type a valid email address'
    return inText
def readMenuChoiceFromKey():
    try:
        inText = int(input("Choice: "))
        return inText
    except KeyboardInterrupt:
        exitProgram()
    except (NameError, SyntaxError):
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Wrong Input, try again!'
        waitEnter()
        return 10
def waitEnter():
    inText = 'a'
    while inText != '':
        try:
            inText = raw_input("Press Enter to continue... ")
            os.system('cls||clear')
            return inText
        except KeyboardInterrupt:
            exitProgram()
        except (NameError, SyntaxError):
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Wrong Input, try again!'
            inText = 'a'
def printScreenHeader():
    global STORE
    os.system('cls||clear')
    print '##################################################'
    print '# Session: ( ', STORE['user']['name'], ' - ', STORE['user']['email'], ' )'
    print '##################################################'
################################################################################
################################################################################
################################################################################
def exitProgram():
    os.system('cls||clear')
    global SERVERCONNECTION
    try:
        SERVERCONNECTION.close()
        print('#################################')
        print '|\tBroZap Burn!\t\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
    except (IndexError, socket.error, EOFError):
        print('#################################')
        print '|\tA Error is raised!\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
    except AttributeError:
        print('#################################')
        print '|\tCant close the comunication!\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
    exit()
def exitProgramWithError():
    os.system('cls||clear')
    global SERVERCONNECTION
    try:
        SERVERCONNECTION.close()
        print('#################################')
        print '|\tBroZap Burn!\t\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
    except (IndexError, socket.error, EOFError):
        print('#################################')
        print '|\tA Error is raised!\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
    except AttributeError:
        print('#################################')
        print '|\tCant close the comunication!\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
    exit()
################################################################################
################################################################################
def connectWithServer():
    global SERVERCONNECTION
    global CONFIG
    count = 0
    while CONFIG['connected'] == False:
        try:
            SERVERCONNECTION = rpyc.connect(
                SERVER_IP,
                SERVER_PORT,
                config = {
                    'allow_public_attrs': True,
                    "allow_pickle": True
                }
            )
            CONFIG['connected'] = True
        except (socket.error, AttributeError):
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: '
            print '\tIt\'s not possible connect with the server'
            print '\tTry Again again!'
            sleep(1)
            count += 1
            if count > 30:
                exitProgramWithError()
################################################################################
################################################################################
#################################### Group ####################################
################################################################################
################################################################################
def remoteGetAllUserGroups():
    pass
def getAllUserGroups():
    pass
def updateGroupStore(newData):
    pass
def printGroupList():
    global STORE
    printScreenHeader()
    print '--------------------------------------------------'
    print '=================== Group List ==================='
    if len(STORE['groups']) > 0:
        for group_id in STORE['groups']:
            printGroup(STORE['groups'][group_id])
    else:
        print '--------------------------------------------------'
        print '+ + + + [Message] -> No groups added'
        print '##################################################'
def printGroup(data):
    print '--------------------------------------------------'
    print '+ Code:', data['id']
    print '+ Name:', data['name']
    print '+ Join at:', data['join_at']
    print '+ Since at:', data['created_at']
    print '--------------------------------------------------'
def remoteAddUserToGroup(group_id):
    try:
        data = SERVERCONNECTION.root.addUserToGroup(user_id=STORE['user']['email'], group_id=group_id)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def enterGroup():
    global STORE
    data = remoteAddUserToGroup(group_id=readGroupIDFromKey())
    if data['type'] == '@GROUP/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Group not found'
        return ''
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    if data['type'] == '@GROUP/DATA':
        STORE['groups'][data['payload']['id']] = data['payload']
        printGroup(data['payload'])
def remoteCreateGroup(group_name):
    try:
        data = SERVERCONNECTION.root.createGroup(user_id=STORE['user']['email'], group_name=group_name)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def createGroup():
    try:
        global STORE
        group_name = readNameFromKey()
        data = remoteCreateGroup(group_name)
        if data['type'] == '@VALIDATION/SMALL_NAME':
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Name to small'
            return ''
        if data['type'] == '@GROUP/CANT_CREATE':
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Cant Create the group'
            return ''
        if data['type'] == '@USER/NOTFOUND':
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: User not found'
            return ''
        if data['type'] == 'ERROR/CONNECTION':
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Connection Error!'
            return ''
        if data['type'] == '@GROUP/DATA':
            STORE['groups'][data['payload']['id']] = data['payload']
            printGroup(data['payload'])
    except AttributeError, e:
        print 'Algo de errado ocorreu: ', e
def printGroupMessages(group_id):
    printScreenHeader()
    print '##################################################'
    print '# Group Chat ', STORE['groups'][group_id]['name']
    print '##################################################'
    if len(STORE['groups'][group_id]['messages']) > 0:
        for message in STORE['groups'][group_id]['messages']:
            print 'De: ', STORE['groups'][group_id]['messages'][message]['sender_id']
            print STORE['groups'][group_id]['messages'][message]['message']
    else:
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No messages yet'
    print '##################################################'
def remoteSendGroupMessage(group_id, message):
    try:
        data = SERVERCONNECTION.root.groupSendMessage(user_id=STORE['user']['email'], group_id=group_id, message=message)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def sendGroupMessege(group_id, message):
    data = remoteSendGroupMessage(group_id, message)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found!'
        return ''
    if data['type'] == '@GROUP/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Group not found!'
        return ''
    if data['type'] == '@GROUP/MESSAGE/ZERO':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No message yet!'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    if data['type'] == '@SERVER/ERROR':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Server Error!'
        return ''
    STORE['groups'][group_id]['messages'] = data['payload']
def remoteGetGroupMessages(group_id):
    try:
        data = SERVERCONNECTION.root.groupMessageHistory(user_id=STORE['user']['email'], group_id=group_id)
        return data
    except (IndexError, socket.error, AttributeError, EOFError, TypeError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def getGroupMessages(group_id):
    data = remoteGetGroupMessages(group_id)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found!'
        return ''
    if data['type'] == '@GROUP/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Group not found!'
        return ''
    if data['type'] == '@GROUP/MESSAGE/ZERO':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No message yet!'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    if data['type'] == '@SERVER/ERROR':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Server Error!'
        return ''
    if data['type'] == '@GROUP/MESSAGE/DATA':
        STORE['groups'][group_id]['messages'] = data['payload']
def groupChatScreen(group_id):
    if group_id not in STORE['groups']:
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: You has no groupd added yet!'
        return ''
    text = ''
    while True:
        try:
            getGroupMessages(group_id)
            printGroupMessages(group_id)
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print "Commands:"
            print "\t[:q] to exit"
            print "\t[:u] to update chat"
            text = raw_input("Text:")
            if text == ':q':
                return ''
            elif text == ':u' or text == '':
                pass
            else:
                sendGroupMessege(group_id, text)
        except KeyboardInterrupt:
            exitProgram()
        except (NameError, SyntaxError), e:
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Wrong Input, try again!'
            print 'Error Message: ', e
            text = ''
            waitEnter()
################################################################################
def groupScreen():
    global STORE
    while True:
        printScreenHeader()
        menuChoice = 10
        print '1 - Create a Group'
        print '2 - Enter in a Group'
        print '3 - List All Your Groups'
        print '4 - Open Group Chat'
        print '0 - Back To Main Screen'
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            createGroup()
        elif menuChoice == 2:
            enterGroup()
        elif menuChoice == 3:
            printGroupList()
        elif menuChoice == 4:
            groupChatScreen(group_id=readGroupIDFromKey())
        elif menuChoice == 0:
            return ''
        waitEnter()
################################################################################
################################################################################
################################################################################
def printAllContacts():
    printScreenHeader()
    print '##################################################'
    print '################## All Contacts ##################'
    print '##################################################'
    if len(STORE['contacts']) > 0:
        for contact in STORE['contacts']:
            print 'Name: ', STORE['contacts'][contact]['name']
            print 'Email: ', STORE['contacts'][contact]['contact_id']
            print '--------------------------------------------------'
    else:
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No contacts yet'
    print '##################################################'
def remoteGetAllUserContacts():
    try:
        data = SERVERCONNECTION.root.getAllUserContacts(user_id=STORE['user']['email'])
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def getAllContacts():
    data = remoteGetAllUserContacts()
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found'
        return ''
    if data['type'] == '@USER/CONTACT/ZERO':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No contacts'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    if data['type'] == '@USER/CONTACT/DATA':
        STORE['contacts'] = data['payload']
def remoteaddContact(contact_id):
    try:
        data = SERVERCONNECTION.root.addContact(user_id=STORE['user']['email'], contact_id=contact_id)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        connectWithServer()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def addContact(contact_id):
    data = remoteaddContact(contact_id=contact_id)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found'
        return ''
    if data['type'] == '@CONTACT/ISALREADY':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Contact is already your friend.'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    print '-> ', contact_id,' now is your friend!'
    STORE['contacts'] = data['payload']
def userContactScreen():
    menuChoice = 10
    global STORE
    while True:
        printScreenHeader()
        print '1 - Add Friend'
        print '2 - All Friends'
        print '0 - Back to main screen'
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            addContact(contact_id=readEmailFromKey())
        elif menuChoice == 2:
            getAllContacts()
            printAllContacts()
        elif menuChoice == 0:
            return ''
        waitEnter()
################################################################################
################################################################################
################################################################################
def printChat(contact_id):
    printScreenHeader()
    print '##################################################'
    print '# Chat with ', contact_id
    print '##################################################'
    if len(STORE['chats'][contact_id]['messages']) > 0:
        for chat_message in STORE['chats'][contact_id]['messages']:
            print 'De: ', STORE['chats'][contact_id]['messages'][chat_message]['sender_id']
            print STORE['chats'][contact_id]['messages'][chat_message]['message']
    else:
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No messages yet'
    print '##################################################'
def remoteSendMessage(contact_id, message):
    try:
        data = SERVERCONNECTION.root.sendMessageUser(user_id=STORE['user']['email'], contact_id=contact_id, message=message)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def sendMessege(contact_id, message):
    data = remoteSendMessage(contact_id, message)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found'
        return ''
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No chat found'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    STORE['chats'][contact_id]['messages'] = data['payload']
def remoteGetMessages(contact_id):
    try:
        data = SERVERCONNECTION.root.chatMessageHistory(user_id=STORE['user']['email'], contact_id=contact_id)
        return data
    except (IndexError, socket.error, AttributeError, EOFError, TypeError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def getMessages(contact_id):
    data = remoteGetMessages(contact_id)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found'
        return ''
    if data['type'] == '@CHAT/MESSAGE/ZERO':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No message yet'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    if data['type'] == '@SERVER/ERROR':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Server Error'
        return ''
    STORE['chats'][contact_id]['messages'] = data['payload']
def remoteCreateChat(contact_id):
    try:
         data = SERVERCONNECTION.root.exposed_createChat(user_id=STORE['user']['email'], contact_id=contact_id)
         return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def createChat(email):
     data = remoteCreateChat(contact_id=email)
     if data['type'] == '@USER/NOTFOUND':
         print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
         print '\tMessage: User not found'
         return ''
     if data['type'] == 'ERROR/CONNECTION':
         print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
         print '\tMessage: Connection Error!'
         return ''
     STORE['chats'] = data['payload']
def userMessageScreen(contact_id):
    if contact_id not in STORE['chats']:
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No friendships, cant send messages!'
        return ''
    if contact_id not in STORE['chats']:
        createChat(contact_id)
    text = ''
    while True:
        try:
            getMessages(contact_id)
            printChat(contact_id)
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print "Commands:"
            print "\t[:q] to exit"
            print "\t[:u] to update chat"
            text = raw_input("Text:")
            if text == ':q':
                return ''
            elif text == ':u':
                pass
            else:
                sendMessege(contact_id, text)
                printChat(contact_id)
        except KeyboardInterrupt:
            exitProgram()
        except (NameError, SyntaxError):
            print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
            print '\tMessage: Wrong Input, try again!'
            text = ''
            waitEnter()
################################################################################
def printChatList():
    global STORE
    print '##################################################'
    print '=================== Chats List ==================='
    if len(STORE['chats']) > 0:
        for chat in STORE['chats']:
            print '--------------------------------------------------'
            print 'Chat With: ', STORE['chats'][chat]['chatWith']
    else:
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: You have not chat yet'
    print '##################################################'
def remoteGetAllUserChats():
    try:
        data = SERVERCONNECTION.root.getAllUserChats(user_id=STORE['user']['email'])
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def getUserChats():
    data = remoteGetAllUserChats()
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: No chat found'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    STORE['chats'] =  data['payload']
def userChatScreen():
    menuChoice = 10
    global STORE
    while True:
        printScreenHeader()
        print '1 - All Chat'
        print '2 - Open Chat'
        print '0 - Back to main screen'
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            getUserChats()
            printChatList()
        elif menuChoice == 2:
            userMessageScreen(contact_id=readEmailFromKey())
        elif menuChoice == 0:
            return ''
        waitEnter()
################################################################################
################################################################################
# MAIN SCREEN
################################################################################
def mainScreen():
    while True:
        printScreenHeader()
        print('1 - Friends Screen')
        print('2 - Chats Screen')
        print('3 - Groups Screen')
        print('0 - Exit BroZap')
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            userContactScreen()
        elif menuChoice == 2:
            userChatScreen()
        elif menuChoice == 3:
            groupScreen()
        elif menuChoice == 0:
            exitProgram()
        else:
            waitEnter
################################################################################
################################################################################
# LOGIN SYSTEM AND CREATE ACCOUNT SYSTEM
################################################################################
def remoteLogOnSystem(email):
    try:
        data = SERVERCONNECTION.root.userLogin(user_id=email)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def logIn(email):
    global STORE
    data = { }
    data = remoteLogOnSystem(email=email)
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: User not found'
        return ''
    STORE = data['payload']
def remoteCreateUser(email, name):
    try:
        data = SERVERCONNECTION.root.createUser(email=email, name=name)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def createAccount():
    print ' ______________________'
    print '|  Welcome BroZap      |'
    print '|  Create new account  |'
    email = readEmailFromKey()
    name = readNameFromKey()
    data = remoteCreateUser(email=email, name=name)
    if data['type'] == '@VALIDATION/NOT_EMAIL':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: It is not a valid email'
        return ''
    if data['type'] == '@VALIDATION/SMALL_NAME':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Name to small'
        return ''
    if data['type'] == '@VALIDATION/EXISTENT':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Choice another account id'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + + + + + + + [Messages] + + + + + + + + + +'
        print '\tMessage: Connection Error!'
        return ''
    STORE['user'] = data['payload']
def loginScreen():
    menuChoice = 10
    while len(STORE['user']) == 0:
        os.system('cls||clear')
        print '#########################'
        print '# 1 - Login\t\t#'
        print '# 2 - Join Us\t\t#'
        print '# 0 - Exit BroZap\t#'
        print '#########################'
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            logIn(readEmailFromKey())
        elif menuChoice == 2:
            createAccount()
        elif menuChoice == 0:
            exitProgram()
        waitEnter()
################################################################################
################################################################################
# MAIN PROGRAM
################################################################################
if __name__ == "__main__":
    global STORE
    global CONFIG
    connectWithServer()
    os.system('cls||clear')
    if CONFIG['connected'] == True:
        loginScreen()
        if len(STORE['user']) > 0:
            mainScreen()
    exitProgram()
