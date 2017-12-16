import sqlite3
from datetime import datetime

def createFriendship(user_email, friend_email):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO friendships (user_id, friend_id, created_at)
        VALUES (?, ?, ?)
    """, (user_email, friend_email, datetime.now()))
    conn.commit()
    conn.close()

def getFriends(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM friendships
        WHERE user = ?
    """,(user_id,))
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects

def all(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM friendships
        WHERE user_id = ?
    """,(user_id,))
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects