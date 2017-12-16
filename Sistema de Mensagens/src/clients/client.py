# -*- coding: utf-8 -*-
import sys, os
import rpyc
import re
SERVER_IP = 'localhost'
SERVER_PORT = 27000
conn = rpyc.connect(SERVER_IP, SERVER_PORT)
USER = {}
FRIENDSHIPS = []
GROUPS = {}
######################################################
def remoteAddFriend(email):
    data = conn.root.createFriendship(email=email)
    return data
def addFriend(email):
    data = remoteAddFriend(email=email)
    if data['type'] == '@USER/NOTFOUND':
        print 'ATENÇÃO: ', data['payload']
        return None
    return data['payload']
def remoteGetFriends():
    data = conn.root.exposed_allFriends()
    return data
def getFriends():
    data = remoteGetFriends()
    if data['type'] == '@USER/NOTFOUND':
        print 'ATENÇÃO: ', data['payload']
        return None
    if data['type'] == '@USER/ZERO':
        print 'ATENÇÃO: ', data['payload']
        return []
    return data['payload']
def findFriend():
    pass
def sendMessege():
    pass
def friendScreen():
    menuChoice = 10
    while menuChoice != 0:
        print('1 - Add Friend')
        print('2 - Get Friend List')
        print('3 - Open Chat')
        print('0 - Sair')
        menuChoice = int(input("Escolha: "))
        if menuChoice is 1:
            email = None
            while email is None:
                email = raw_input("Email: ")
                if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
                    print 'ATENÇÃO -> Por Favor digite um e-mail Valido!'
                    email = None
                else:
                    FRIENDSHIPS = addFriend(email)
        elif menuChoice is 2:
            FRIENDSHIPS = getFriends()
        elif menuChoice is 3:
            pass
        else:
            pass

######################################################
def userScreen():
    menuChoice = -1
    while menuChoice != 0:
        print('1 - Friend List')
        print('2 - Group List')
        print('0 - Sair')
        menuChoice = int(input("Escolha: "))
        if menuChoice is 1:
            friendScreen()
        elif menuChoice is 2:
            pass
        else:
            pass
###################################################
def remoteLogOnSystem(email):
    user = conn.root.userLogin(email=email)
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
    print('##################')
    print('# 1 - Logar')
    print('# 2 - Criar Conta')
    print('# 0 - Sair')
    print('##################')
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
        os.system('cls||clear')
        print('Programa finalizado com sucesso!')
        conn.close()
        exit()

if __name__ == "__main__":
    os.system('cls||clear')
    USER = loginScreen()
    print('Usuario: ',USER)
    if(USER):
        os.system('cls||clear')
        userScreen()
    conn.close()