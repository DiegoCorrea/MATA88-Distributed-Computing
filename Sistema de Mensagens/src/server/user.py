class User:
    name = ''
    id = 0
    groupList = []
    def __init__(self, id, name):
        self.id = id
        self.name = name
        pass
    def getId(self):
        return self.id
    def getGroupList(self):
        return self.groupList
    def addGroup(self, newGroup):
        self.groupList.append(newGroup)
        return self.groupList
