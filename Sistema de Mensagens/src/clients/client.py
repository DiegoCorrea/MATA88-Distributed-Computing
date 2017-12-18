# -*- coding: utf-8 -*-
import sys, os
import rpyc
import re
SERVER_IP = 'localhost'
SERVER_PORT = 27000
conn = rpyc.connect(SERVER_IP, SERVER_PORT)
USER = { }
FRIENDSHIP = { }
CHATS = { }
GROUPS = { }
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
    print 'Sessão: ( ', USER['name'], ' - ', USER['email'], ' )'
    print '##################################################'
################################################################################
################################################################################
################################################################################
def remoteAddFriend(friend_id):
    data = conn.root.exposed_createChat(user_id=USER['email'], friend_id=friend_id)
    return data
def addFriend(email):
    data = remoteAddFriend(friend_id=email)
    if data['type'] == '@USER/NOTFOUND':
        print 'ATENÇÃO: ', data['payload']
        return None
    return data['payload']
def userFriendScreen():
    menuChoice = 10
    global FRIENDSHIP
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
                    print 'ATENÇÃO -> Por Favor digite um e-mail Valido!'
                    email = None
                else:
                    FRIENDSHIP = addFriend(email)
################################################################################
################################################################################
################################################################################
def printChat(chatHistory):
    printScreenHeader()
    print '##################################################'
    print 'Historico de conversa com '
    print '##################################################'
    for chat_message in chatHistory:
        print 'De: ', chatHistory[chat_message]['sender_id']
        print chatHistory[chat_message]['message']
    print '##################################################'
def remoteSendMessage(friend_id, message):
    data = conn.root.sendMessageUser(user_id=USER['email'], friend_id=friend_id, message=message)
    return data
def sendMessege(friend_id, message):
    data = remoteSendMessage(friend_id, message)
    return data['payload']
def remoteGetMessages(friend_id):
    data = conn.root.chatMessageHistory(user_id=USER['email'], friend_id=friend_id)
    return data
def getMessages(email):
    data = remoteGetMessages(email)
    if data['type'] == '@CHAT/ZERO':
        print 'ATENÇÃO: Não existem mensagens no Chat'
    return data['payload']
def userMessageScreen(email):
    if email not in CHATS:
        print '+ + + + ATENÇÃO: Não existe amizade entre as partes!'
        return None
    printChat(getMessages(email))
    text = raw_input("Digite o texto de envio: ")
    printChat(sendMessege(email, text))
################################################################################
def printChatList():
    print '##################################################'
    for chat in CHATS:
        print 'Chat With: ', CHATS[chat]['chatWith']
    print '##################################################'
def remoteGetAllUserChats():
    data = conn.root.allChats(user_id=USER['email'],)
    return data
def getUserChats():
    data = remoteGetAllUserChats()
    if data['type'] == '@CHAT/NOTFOUND':
        print '+ + + + ATENÇÃO: Chat não encontrado'
        return { }
    if data['type'] == '@CHAT/ZERO':
        print '+ + + + ATENÇÃO: Você ainda não conversou com ninguém'
        return { }
    return data['payload']
################################################################################
def userChatScreen():
    menuChoice = 10
    global CHATS
    while menuChoice != 0:
        printScreenHeader()
        print('1 - All Chat')
        print('2 - Open Chat')
        print('0 - Back to main screen')
        menuChoice = int(input("Choice: "))
        if menuChoice is 1:
            CHATS = getUserChats()
            if len(CHATS) > 0:
                printChatList()
            waitEnter()
        elif menuChoice is 2:
            email = None
            while email is None:
                email = raw_input("Open chat with: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    print 'ATENÇÃO -> Por Favor digite um e-mail Valido!'
                    email = None
                else:
                    userMessageScreen(email=email)
                    waitEnter()
        else:
            pass
################################################################################
################################################################################
################################################################################
def mainScreen():
    menuChoice = -1
    while menuChoice != 0:
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
            pass
        elif menuChoice is 0:
            exitProgram()
        else:
            pass
################################################################################
################################################################################
################################################################################
def remoteLogOnSystem(email):
    user = conn.root.userLogin(user_id=email)
    return user
def logIn(email):
    if(re.match(r"[^@]+@[^@]+\.[^@]+", email) == None):
        print('ATENÇÃO -> Por Favor digite um e-mail Valido!')
        return None
    user = remoteLogOnSystem(email=email)
    if(user['type'] == '@USER/NOTFOUND'):
        print('ATENÇÃO -> ', user['payload'])
        return None
    return user['payload']
def remoteCreateUser(email, name):
    data = conn.root.createUser(email=email, name=name)
    return data
def createAccount(email, name):
    if(re.match(r"[^@]+@[^@]+\.[^@]+", email) == None):
        print('ATENÇÃO -> Por Favor digite um e-mail Valido!')
        return None
    if(len(name) < 3):
        print('ATENÇÃO -> Um nome maior que 3 letras é necessario')
        return None
    data = remoteCreateUser(email=email, name=name)
    if (data['type'] == 'VALIDATION/ERROR'):
        print('ATENÇÃO: ', data['payload'])
        return None
    return data['payload']
def loginScreen():
    print('#########################')
    print('# 1 - Logar\t\t#')
    print('# 2 - Criar Conta\t#')
    print('# 0 - Sair\t\t#')
    print('#########################')
    loginChoice = int(input("Escolha: "))
    if(loginChoice == 1):
        user = None
        while(user == None):
            email = raw_input("Email: ")
            user = logIn(email)
        return user
    elif(loginChoice == 2):
        newUser = None
        while(newUser == None):
            print('Cadastrar nova conta')
            email = raw_input("Email: ")
            name = raw_input("Nome: ")
            newUser = createAccount(email=email, name=name)
        return newUser
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
    global USER
    global CHATS
    os.system('cls||clear')
    USER = loginScreen()
    if(USER):
        CHATS = getUserChats()
        mainScreen()
    exitProgram()
