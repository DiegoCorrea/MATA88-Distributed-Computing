# -*- coding: utf-8 -*-
import sys, os
import rpyc
import re
SERVER_IP = 'localhost'
SERVER_PORT = 27000
conn = rpyc.connect(SERVER_IP, SERVER_PORT)
STORE = {
    'user': { },
    'friendships': { },
    'chats': { },
    'groups': { }
}
################################################################################
################################################################################
################################################################################
def printGroupList():
    printScreenHeader()
    print '##################################################'
    print 'Group List'
    print '--------------------------------------------------'
    if len(STORE['groups']) > 0:
        for group_id in STORE['groups']:
            print 'Group CODE: % ', STORE['groups'][group_id]['group_id'], ' %'
            print 'Group Name: ', STORE['groups'][group_id]['name']
            print 'Join At:', STORE['groups'][group_id]['join_at'], '|| Group since: ', STORE['groups'][group_id]['created_at']
            print '--------------------------------------------------'
    else:
        print 'No groups added'
    print '##################################################'
def remoteCreateGroup(group_name):
    data = conn.root.createGroup(STORE['user']['email'], group_name)
    return data
def createGroup():
    group_name = raw_input("Give a name: ")
    data = remoteCreateGroup(group_name)
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
            pass
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
def waitEnter():
    menuChoice = 'a'
    while menuChoice != '':
        menuChoice = raw_input("Precione Enter para sair")
    os.system('cls||clear')
################################################################################
################################################################################
################################################################################
def printScreenHeader():
    os.system('cls||clear')
    print '##################################################'
    print 'Session: ( ', STORE['user']['name'], ' - ', STORE['user']['email'], ' )'
    print '##################################################'
################################################################################
################################################################################
################################################################################
def remoteAddFriend(friend_id):
    data = conn.root.exposed_createChat(user_id=STORE['user']['email'], friend_id=friend_id)
    return data
def addFriend(email):
    data = remoteAddFriend(friend_id=email)
    if data['type'] == '@USER/NOTFOUND':
        print '[ALERT]: ', data['payload']
        return { }
    return data['payload']
def userFriendScreen():
    menuChoice = 10
    global STORE
    while menuChoice != 0:
        printScreenHeader()
        print('1 - Add Friend')
        print('2 - All Friends')
        print('0 - Back to main screen')
        menuChoice = int(input("Choice: "))
        if menuChoice is 1:
            email = None
            while email is None:
                email = raw_input("Email: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    print '+ + + + [ALERT] -> Por Favor digite um e-mail Valido!'
                    email = None
                else:
                    STORE['friendships'] = addFriend(email)
################################################################################
################################################################################
################################################################################
def printChat(friend_id):
    printScreenHeader()
    print '##################################################'
    print 'Historico de conversa com ', friend_id
    print '##################################################'
    for chat_message in STORE['chats'][friend_id]['messages']:
        print 'De: ', STORE['chats'][friend_id]['messages'][chat_message]['sender_id']
        print STORE['chats'][friend_id]['messages'][chat_message]['message']
    print '##################################################'
def remoteSendMessage(friend_id, message):
    data = conn.root.sendMessageUser(user_id=STORE['user']['email'], friend_id=friend_id, message=message)
    return data
def sendMessege(friend_id, message):
    data = remoteSendMessage(friend_id, message)
    STORE['chats'][friend_id]['messages'] = data['payload']
    return True
def remoteGetMessages(friend_id):
    data = conn.root.chatMessageHistory(user_id=STORE['user']['email'], friend_id=friend_id)
    return data
def getMessages(friend_id):
    data = remoteGetMessages(friend_id)
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + [ALERT]: Não existem mensagens no Chat'
        return False
    STORE['chats'][friend_id]['messages'] = data['payload']
    return True
def userMessageScreen(friend_id):
    if friend_id not in STORE['chats']:
        print '+ + + + [ALERT]: Não existe amizade entre as partes!'
        return False
    text = ''
    while True:
        getMessages(friend_id)
        printChat(friend_id)
        text = raw_input("Digite o texto de envio: ")
        if text != ':q':
            sendMessege(friend_id, text)
            printChat(friend_id)
        else:
            return True
################################################################################
def printChatList():
    print '##################################################'
    for chat in STORE['chats']:
        print 'Chat With: ', STORE['chats'][chat]['chatWith']
    print '##################################################'
def remoteGetAllUserChats():
    data = conn.root.allChats(user_id=STORE['user']['email'])
    return data
def getUserChats():
    data = remoteGetAllUserChats()
    if data['type'] == '@CHAT/NOTFOUND':
        print '+ + + + [ALERT]: Chat não encontrado'
        return { }
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + [ALERT]: Você ainda não conversou com ninguém'
        return { }
    return data['payload']
################################################################################
def userChatScreen():
    menuChoice = 10
    global STORE
    while menuChoice != 0:
        printScreenHeader()
        print '1 - All Chat'
        print '2 - Open Chat'
        print '0 - Back to main screen'
        menuChoice = int(input("Choice: "))
        if menuChoice is 1:
            STORE['chats'] = getUserChats()
            if len(STORE['chats']) > 0:
                printChatList()
            waitEnter()
        elif menuChoice is 2:
            email = None
            while email is None:
                email = raw_input("Open chat with: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    print '[ALERT] -> Por Favor digite um e-mail Valido!'
                    email = None
                else:
                    userMessageScreen(friend_id=email)
                waitEnter()
        else:
            pass
################################################################################
################################################################################
################################################################################
def mainScreen():
    while True:
        menuChoice = None
        printScreenHeader()
        print('1 - Friends Screen')
        print('2 - Chats Screen')
        print('3 - Groups Screen')
        print('0 - Exit BroZap')
        menuChoice = int(input("Choice: "))
        if menuChoice is 1:
            userFriendScreen()
        elif menuChoice is 2:
            userChatScreen()
        elif menuChoice is 3:
            groupScreen()
        elif menuChoice is 0:
            exitProgram()
        else:
            pass
################################################################################
################################################################################
################################################################################
def remoteLogOnSystem(email):
    data = conn.root.userLogin(user_id=email)
    return data
def logIn(email):
    global STORE
    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print '+ + + + [ALERT] -> Por Favor digite um e-mail Valido!'
        return False
    data = remoteLogOnSystem(email=email)
    if data['type'] == '@USER/NOTFOUND':
        print '+ + + + [ALERT] -> Usuario nao encontrado'
        return False
    STORE = data['payload']
    return True
def remoteCreateUser(email, name):
    data = conn.root.createUser(email=email, name=name)
    return data
def createAccount(email, name):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print '+ + + + [ALERT] -> Por Favor digite um e-mail Valido!'
        return False
    if len(name) < 3:
        print '+ + + + [ALERT] -> Um nome maior que 3 letras eh necessario'
        return False
    data = remoteCreateUser(email=email, name=name)
    if data['type'] == 'VALIDATION/ERROR':
        print '+ + + + [ALERT] -> Erro na validacao '
        return False
    STORE['user'] = data['payload']
    return True
def loginScreen():
    print '#########################'
    print '# 1 - Login\t\t#'
    print '# 2 - Join Us\t#'
    print '# 0 - Exit BroZap\t\t#'
    print '#########################'
    loginChoice = int(input("Choice: "))
    if loginChoice == 1:
        loopTruth = False
        while loopTruth is False:
            email = raw_input("Open chat with: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                print '+ + + + [ALERT] -> Por Favor digite um e-mail Valido!'
                loopTruth = False
            else:
                loopTruth = logIn(email)
    elif loginChoice == 2:
        loopTruth = False
        while loopTruth is False:
            print 'Create new account'
            email = raw_input("Email: ")
            name = raw_input("Name: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                print '+ + + + [ALERT] -> Por Favor digite um e-mail Valido!'
                loopTruth = False
            else:
                loopTruth = createAccount(email=email, name=name)
    else:
        exitProgram()
################################################################################
################################################################################
################################################################################
def exitProgram():
    os.system('cls||clear')
    print('#################################')
    print '|\tBroZap Finalizado!\t|'
    print '|\tTe vemos na proxima\t|'
    print('#################################')
    conn.close()
    exit()
################################################################################
################################################################################
################################################################################
if __name__ == "__main__":
    global STORE
    os.system('cls||clear')
    loginScreen()
    if len(STORE['user']) > 0:
        mainScreen()
    exitProgram()
