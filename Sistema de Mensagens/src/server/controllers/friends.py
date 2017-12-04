import sqlite3
from datetime import datetime
def createFriendship(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO friendship (user, friend, friends_at)
        VALUES (?, ?, ?)
    """, (user_id, friend_id, datetime.now()))
    conn.commit()
    conn.close()

def getFriendsList(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM friendship
    WHERE user = ?
    """,(user_id,))
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects
