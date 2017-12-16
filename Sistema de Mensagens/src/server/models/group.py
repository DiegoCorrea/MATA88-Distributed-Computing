import uuid

class Group:
    name = ''
    id = ''
    memberList = []
    adminList = []
    def __init__(self, name):
        self.id =  uuid.uuid1()
        self.name = name
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getMembersList(self):
        return self.memberList
    def addMember(self, newMember):
        self.memberList.append(newMember)
        return self.memberList
