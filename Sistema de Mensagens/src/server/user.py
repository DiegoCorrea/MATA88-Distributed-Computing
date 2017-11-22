import uuid

class User:
    name = ''
    id = ''
    groupList = []
    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
        pass
    def getId(self):
        return self.id
    def getName(self)
        return self.name
    def getGroupList(self):
        return self.groupList
    def addGroup(self, newGroup):
        self.groupList.append(newGroup)
        return self.groupList
