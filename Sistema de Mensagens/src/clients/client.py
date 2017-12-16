# -*- coding: utf-8 -*-
import sys, os
import rpyc
import re
SERVER_IP = 'localhost'
SERVER_PORT = 27000
conn = rpyc.connect(SERVER_IP, SERVER_PORT)
USER = {}

######################################################
def addFriend():
    pass
def getFriends():
    pass
def findFriend():
    pass
def sendMessege():
    pass
def friendScreen():
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
    user = conn.root.userLogin(email)
    return user
def logIn(email):
    if(re.match(r"[^@]+@[^@]+\.[^@]+", email) == ''):
        print('ATENÇÃO -> Por Favor digite um e-mail Valido!')
        return None
    user = remoteLogOnSystem(email)
    if(user['type'] == '@USER/NOTFOUND'):
        print('ATENÇÃO -> ', user['payload'])
    return user['payload']
def remoteCreateUser(email, name):
    userData = conn.root.createUser(email, name)
    return userData
def createAccount(email, name):
    if(re.match(r"[^@]+@[^@]+\.[^@]+", email) == ''):
        print('ATENÇÃO -> Por Favor digite um e-mail Valido!')
        return None
    if(len(name) < 3):
        print('ATENÇÃO -> Um nome maior que 3 letras é necessario')
        return None
    userData = remoteCreateUser(email, name)
    if (userData['type'] == 'VALIDATION/ERROR'):
        print('ATENÇÃO: ', userData['payload'])
        return None
    return userData['payload']
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
            newUser = createAccount(name, email)
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