import sys
import rpyc
from configs import SERVER_IP, SERVER_PORT

def groupMenu():
    userName = ''
    print('1 - Criar Grupo')
    print('2 - Listar Meus Grupos')
    print('3 - Buscar um Grupo')
    print('4 - Entrar em um Grupo')
    print('0 - Sair')
    menuChoice = int(input("Escolha: "))
    return menuChoice

def makeGroup():
    groupName = ''
    groupName = raw_input("Novo Grupo: ")
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    newgroup = conn.root.createGroup(groupName)
    conn.close()

def allGroups():
    conn = rpyc.connect(SERVER_IP, SERVER_PORT)
    groups = conn.root.allGroupsList()
    print('\t\t---- All Groups ----')
    print('Action type: ', groups['type'])
    for group in groups['payload']:
        print('ID: ', group['id'])
        print('Name: ', group['name'])
    print('\n\n')
    conn.close()

def groupScreen():
    menuChoice = groupMenu()
    while menuChoice != 0:
        if menuChoice is 1:
            makeGroup()
        elif menuChoice is 2:
            allGroups()
        else:
            pass
        menuChoice = groupMenu()