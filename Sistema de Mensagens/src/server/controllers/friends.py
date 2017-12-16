import sqlite3
import uuid
from datetime import datetime

def createFriendship(user_email, friend_email):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO friendships (id, user_id, friend_id, created_at)
        VALUES (?, ?, ?, ?)
    """, (str(uuid.uuid4()), user_email, friend_email, datetime.now()))
    conn.commit()
    conn.close()

def getFriends(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT friend_id, created_at FROM friendships
        WHERE user_id = ?
    """, user_id)
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects

def all(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT friend_id, created_at FROM friendships
        WHERE user_id = ?;
    """, (user_id,))
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects
