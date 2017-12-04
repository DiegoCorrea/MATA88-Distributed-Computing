import sys
import rpyc

SERVER_IP = 'localhost'
SERVER_PORT = 27000

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
    print('2 - Listar Usuarios')
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

def allUser():
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    users = conn.root.allUsersList()
    print('users: ', users)
    #for user in users:
    #    print('ID: ', user.value())
    #    print('Name: ', user.User.getName())
    conn.close()

def userScreen():
    menuChoice = userMenu()
    while menuChoice != 0:
        if menuChoice is 1:
            makeUser()
        elif menuChoice is 2:
            allUser()
        else:
            pass
        menuChoice = userMenu()
def logOnSystem(loginIdentifier):
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    user = conn.root.loginUser(loginIdentifier)
    conn.close()
def loginScreen():
    print('##################')
    print('# 1 - Logar')
    print('# 2 - Criar Conta')
    print('# 0 - Sair')
    print('##################')
    loginChoice = int(input("Escolha: "))
    if(loginChoice == 1):
        loginIdentifier = int(input("Digite o identificador: "))
        return logOnSystem(loginIdentifier)
    elif(loginChoice == 2):
        pass
    else:
        exit()

if __name__ == "__main__":
    userScreen()
