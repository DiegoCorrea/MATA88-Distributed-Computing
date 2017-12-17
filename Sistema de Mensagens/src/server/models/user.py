import sqlite3
from datetime import datetime

class User:
    name = ''
    email = ''
    created_at = ''
    updated_at = ''
    groupList = []
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def getName(self):
        return self.name
    def getID(self):
        return self.email
    def getemail(self):
        return self.email
    def save(self):
        conn = sqlite3.connect('./db/whatsApp.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (self.name, self.email, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()
