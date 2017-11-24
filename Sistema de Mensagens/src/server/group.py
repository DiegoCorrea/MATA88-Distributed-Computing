import uuid
import logging

class Group:
    name = ''
    id = ''
    memberList = []
    adminList = []
    def __init__(self, name):
        logging.info('[Group __init__] Start')
        self.id =  uuid.uuid1()
        self.name = name
        logging.info('[Group __init__] End')
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getMembersList(self):
        return self.memberList
    def addMember(self, newMember):
        self.memberList.append(newMember)
        return self.memberList
