# -*- coding: utf-8 -*-
import sys, os
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
################################################################################
################################################################################
################################################################################
def remoteAddUserToGroup(group_id):
    data = SERVERCONNECTION.root.addUserToGroup(STORE['user']['email'], group_id)
    return data
def enterGroup():
    group_id = raw_input("Group ID: ")
    data = remoteAddUserToGroup(group_id)
    if data['type'] == '@GROUP/NOTFOUND':
        print '+ + + + [ALERT] -> Group not found'
        return { }
    if data['type'] == '@GROUP/ZERO':
        print '+ + + + [ALERT] -> Cant Create the group'
        return { }
    STORE['groups'] = data['payload']
    print 'Group created successfully!'
def printGroupList():
    printScreenHeader()
    print '##################################################'
    print 'Group List'
    print '--------------------------------------------------'
    if len(STORE['groups']) != 0:
        for group_id in STORE['groups']:
            print 'Group CODE: % ', STORE['groups'][group_id]['group_id'], ' %'
            print 'Group Name: ', STORE['groups'][group_id]['name']
            print 'Join At:', STORE['groups'][group_id]['join_at'], '|| Group since: ', STORE['groups'][group_id]['created_at']
            print '--------------------------------------------------'
    else:
        print 'No groups added'
    print '##################################################'
def remoteCreateGroup(group_name):
    data = SERVERCONNECTION.root.createGroup(STORE['user']['email'], group_name)
    return data
def createGroup():
    group_name = raw_input("Give a name: ")
    data = remoteCreateGroup(group_name)
    if data['type'] == '@VALIDATION/SMALL_NAME':
        print '+ + + + [ALERT] -> Name to small'
        return { }
    if data['type'] == '@GROUP/ZERO':
        print '+ + + + [ALERT] -> Cant Create the group'
        return { }
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + [ALERT] -> User not found'
        return { }
    STORE['groups'] = data['payload']
    print 'Group created successfully!'
################################################################################
def groupScreen():
    menuChoice = 10
    global STORE
    while menuChoice != 0:
        printScreenHeader()
        print '1 - Create a Group'
        print '2 - Enter in a Group'
        print '3 - List All Your Groups'
        print '4 - Open Group Chat'
        print '0 - Back To Main Screen'
        menuChoice = int(input("Choice: "))
        if menuChoice is 1:
            createGroup()
            waitEnter()
        elif menuChoice is 2:
            enterGroup()
        elif menuChoice is 3:
            printGroupList()
            waitEnter()
        elif menuChoice is 4:
            pass
        else:
            pass
################################################################################
################################################################################
################################################################################
def readEmailFromKey():
    email = ''
    while email == '':
        try:
            email = raw_input("Email: ")
        except KeyboardInterrupt:
            exitProgram()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
            print '+ + + + [ALERT] -> Please type a valid email address'
            email = ''
    return email
def readMenuChoiceFromKey():
    try:
        menuChoice = int(input("Choice: "))
        return menuChoice
    except KeyboardInterrupt:
        exitProgram()
    except NameError:
        print '+ + + + [ALERT] -> Wrong Input, try again!'
        waitEnter()
        return 10
def waitEnter():
    menuChoice = 'a'
    while menuChoice != '':
        menuChoice = raw_input("Press Enter to continue...")
    os.system('cls||clear')

################################################################################
################################################################################
################################################################################
def printScreenHeader():
    os.system('cls||clear')
    print '##################################################'
    print '# Session: ( ', STORE['user']['name'], ' - ', STORE['user']['email'], ' )'
    print '##################################################'
################################################################################
################################################################################
################################################################################
def printAllContacts():
    printScreenHeader()
    print '##################################################'
    print '# All Contacts'
    print '##################################################'
    if len(STORE['contacts']) != 0:
        for contact in STORE['contacts']:
            print 'Name: ', STORE['contacts'][contact]
            print 'Email: ', STORE['contacts'][contact]
            print '--------------------------------------------------'
    else:
        print 'No contacts yet'
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
        print '+ + + + [ALERT]: User not found'
        return ''
    if data['payload'] == '@USER/CONTACT/ZERO':
        print '+ + + + [ALERT]: No contacts'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + [ALERT] -> Connection Error!'
        return ''
    STORE['contacts'] = data['payload']
    printAllContacts()
    return ''
def remoteaddContact(contact_id):
    try:
        data = SERVERCONNECTION.root.addContact(user_id=STORE['user']['email'], contact_id=contact_id)
        return data
    except (IndexError, socket.error, AttributeError, EOFError):
        return {
            'type': 'ERROR/CONNECTION',
            'payload': { }
        }
def addContact(contact_id):
    data = remoteaddContact(contact_id=contact_id)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + [ALERT]: User not found'
        return ''
    if data['type'] == '@CONTACT/ISALREADY':
        print '+ + + + [ALERT]: Contact is already your friend.'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + [ALERT] -> Connection Error!'
        return ''
    print '-> ', contact_id,' now is your friend!'
    STORE['contacts'] = data['payload']
    return ''
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
        elif menuChoice == 0:
            return ''
        waitEnter()
################################################################################
################################################################################
################################################################################
def printChat(friend_id):
    printScreenHeader()
    print '##################################################'
    print '# Chat with ', friend_id
    print '##################################################'
    if len(STORE['chats'][friend_id]['messages']) != 0:
        for chat_message in STORE['chats'][friend_id]['messages']:
            print 'De: ', STORE['chats'][friend_id]['messages'][chat_message]['sender_id']
            print STORE['chats'][friend_id]['messages'][chat_message]['message']
    else:
        print 'No messages yet'
    print '##################################################'
def remoteSendMessage(friend_id, message):
    data = SERVERCONNECTION.root.sendMessageUser(user_id=STORE['user']['email'], friend_id=friend_id, message=message)
    return data
def sendMessege(friend_id, message):
    data = remoteSendMessage(friend_id, message)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + [ALERT] -> User not found'
        return False
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + [ALERT]: No chat found'
        return False
    STORE['chats'][friend_id]['messages'] = data['payload']
    return True
def remoteGetMessages(friend_id):
    data = SERVERCONNECTION.root.chatMessageHistory(user_id=STORE['user']['email'], friend_id=friend_id)
    return data
def getMessages(friend_id):
    data = remoteGetMessages(friend_id)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + [ALERT] -> User not found'
        return False
    if data['type'] == '@CHAT/MESSAGE/ZERO':
        print '+ + + + [ALERT]: No message yet'
        return False
    STORE['chats'][friend_id]['messages'] = data['payload']
    return True
def remoteCreateChat(friend_id):
     data = SERVERCONNECTION.root.exposed_createChat(user_id=STORE['user']['email'], friend_id=friend_id)
     return data
def createChat(email):
     data = remoteCreateChat(friend_id=email)
     if data['type'] == '@USER/NOTFOUND':
         print '[ALERT]: ', data['payload']
         return ''
     STORE['chats'] = data['payload']
     return ''
def userMessageScreen(friend_id):
    if friend_id not in STORE['contacts']:
        print '+ + + + [ALERT]: No friendships, cant send messages!'
        return False
    if friend_id not in STORE['chats']:
        createChat(friend_id)
    text = ''
    while True:
        getMessages(friend_id)
        printChat(friend_id)
        text = raw_input("Text to send (':q' to exit): ")
        if text != ':q':
            sendMessege(friend_id, text)
            printChat(friend_id)
        else:
            return True
################################################################################
def printChatList():
    print '##################################################'
    print '= Chat List ='
    print '##################################################'
    if len(STORE['chats']) != 0:
        for chat in STORE['chats']:
            print 'Chat With: ', STORE['chats'][chat]['chatWith']
            print '--------------------------------------------------'
    else:
        print 'You has no chats!'
    print '##################################################'
def remoteGetAllUserChats():
    data = SERVERCONNECTION.root.allChats(user_id=STORE['user']['email'])
    return data
def getUserChats():
    data = remoteGetAllUserChats()
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + [ALERT]: No chat found'
        return { }
    return data['payload']
def userChatScreen():
    menuChoice = 10
    global STORE
    while menuChoice != 0:
        printScreenHeader()
        print '1 - All Chat'
        print '2 - Open Chat'
        print '0 - Back to main screen'
        menuChoice = int(input("Choice: "))
        if menuChoice == 1:
            STORE['chats'] = getUserChats()
            printChatList()
        elif menuChoice == 2:
            email = None
            while email == None:
                email = raw_input("Open chat with: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    print '+ + + + [ALERT] -> Please type a valid email address'
                    email = None
                else:
                    userMessageScreen(friend_id=email)
        waitEnter()
################################################################################
################################################################################
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
            pass
################################################################################
################################################################################
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
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + [ALERT] -> User not found'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + [ALERT] -> Connection Error!'
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
    name = ''
    try:
        name = raw_input("Name: ")
    except KeyboardInterrupt:
        exitProgram()
    except NameError:
        menuChoice = 10
        print '+ + + + [ALERT] -> Wrong Input, try again!'
    data = remoteCreateUser(email=email, name=name)
    if data['type'] == '@VALIDATION/NOT_EMAIL':
        print '+ + + + [ALERT] -> It is not a valid email'
        return ''
    if data['type'] == '@VALIDATION/SMALL_NAME':
        print '+ + + + [ALERT] -> Name to small'
        return ''
    if data['type'] == '@VALIDATION/EXISTENT':
        print '+ + + + [ALERT] -> Choice another account id'
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print '+ + + + [ALERT] -> Connection Error!'
        return ''
    STORE['user'] = data['payload']
def loginScreen():
    print '#########################'
    print '# 1 - Login\t\t#'
    print '# 2 - Join Us\t\t#'
    print '# 0 - Exit BroZap\t#'
    print '#########################'
    menuChoice = 10
    while len(STORE['user']) == 0:
        try:
            menuChoice = int(input("Choice: "))
        except KeyboardInterrupt:
            exitProgram()
        except NameError:
            menuChoice = 10
            print '+ + + + [ALERT] -> Wrong Input, try again!'
        if menuChoice == 1:
            logIn(readEmailFromKey())
        elif menuChoice == 2:
            createAccount()
        elif menuChoice == 0:
            exitProgram()
################################################################################
################################################################################
################################################################################
def exitProgram():
    os.system('cls||clear')
    try:
        SERVERCONNECTION.close()
        print('#################################')
        print '|\tBroZap Burn!\t\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
        exit()
    except (IndexError, socket.error, AttributeError, EOFError):
        print('#################################')
        print '|\tA Error is raised!\t|'
        print '|\tTchuss!\t\t\t|'
        print('#################################')
        exit()
################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    try:
        SERVERCONNECTION = rpyc.connect(SERVER_IP, SERVER_PORT)
    except socket.error, AttributeError:
        exitProgram()
    global STORE
    os.system('cls||clear')
    loginScreen()
    if len(STORE['user']) > 0:
        mainScreen()
    exitProgram()
