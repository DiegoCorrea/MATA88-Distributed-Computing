import uuid
import sqlite3
from datetime import datetime

class User:
    name = ''
    id = ''
    email = ''
    created_at = ''
    updated_at = ''
    groupList = []
    def __init__(self, _id, name, email):
        if(_id != None):
            self.id = _id
        else:
            self.id = str(uuid.uuid1())
        self.name = name
        self.email = email
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getemail(self):
        return self.email
    def save(self):
        conn = sqlite3.connect('./db/whatsApp.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, name, email, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (self.id, self.name, self.email, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()