import sys
import rpyc
from configs import SERVER_IP, SERVER_PORT
from groupManager import groupScreen, makeGroup, allGroups

def callCreateUser(userName):
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    newUser = conn.root.createUser(userName)
    conn.close()
    return newUser

def printMenu():
    print('\t---- Menu ----')
    print('1 - Usuarios')
    print('2 - Grupos')
    print('0 - Sair')

def userMenu():
    userName = ''
    print('1 - Criar Usuario')
    print('2 - Listar Amigos')
    print('3 - Listar Grupos')
    print('4 - Criar Grupos')
    print('0 - Sair')
    menuChoice = int(input("Escolha: "))
    return menuChoice

def isUser():
    userName = ''
    while(len(userName) < 5):
        print("\nDigite o seu login: ")
        userName = sys.stdin.readline()
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    user = conn.root.findUserByName(userName)
    conn.close()
    return user

def makeUser():
    loginName = ''
    loginName = raw_input("Novo Usuario: ")
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    user = conn.root.createUser(loginName)
    conn.close()

def userFriends():
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    users = conn.root.allUsersFriends()
    print('\t\t---- User Friends ----')
    print('Action type: ', users['type'])
    for user in users['payload']:
        print('ID: ', user['id'])
        print('Name: ', user['name'])
    print('\n\n')
    conn.close()
def userGroups():
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    groups = conn.root.allUsersGroups()
    print('\t\t---- User Group ----')
    print('Action type: ', groups['type'])
    for group in groups['payload']:
        print('ID: ', group['id'])
        print('Name: ', group['name'])
    print('\n\n')
    conn.close()

def userScreen():
    menuChoice = userMenu()
    while menuChoice != 0:
        if menuChoice is 1:
            makeUser()
        elif menuChoice is 2:
            userFriends()
        elif menuChoice is 3:
            allGroups()
        elif menuChoice is 4:
            makeGroup()
        else:
            pass
        menuChoice = userMenu()

if __name__ == "__main__":
    userScreen()
