import sqlite3
import sys
sys.path.append('..')
from models.user import User

def all():
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users;
    """)
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects

def findBy_email(email):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE email=?;
    """, (email,))
    returnedObject = cursor.fetchone()
    if(returnedObject):
        user = User(email=returnedObject[2], _id=returnedObject[0], name=returnedObject[1])
        conn.close()
        return user
    return None