import uuid
import logging

class User:
    name = ''
    id = ''
    groupList = []
    def __init__(self, name):
        logging.info('[User __init__] Inicio')
        self.id =  uuid.uuid1()
        self.name = name
        logging.info('[User __init__] Fim')
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getGroupList(self):
        return self.groupList
    def addGroup(self, newGroup):
        self.groupList.append(newGroup)
        return self.groupList
