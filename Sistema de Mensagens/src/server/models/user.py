import uuid
import sqlite3
from datetime import datetime
class User:
    name = ''
    id = ''
    groupList = []
    def __init__(self, name):
        self.id =  str(uuid.uuid1())
        self.name = name
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getGroupList(self):
        return self.groupList
    def addGroup(self, newGroup):
        self.groupList.append(newGroup)
        return self.groupList
    def save(self):
        conn = sqlite3.connect('./db/whatsApp.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, loginName, join_at)
            VALUES (?, ?, ?)
        """, (self.id, self.name, datetime.now()))
        conn.commit()
        conn.close()