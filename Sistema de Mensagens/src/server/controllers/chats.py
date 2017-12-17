import sqlite3
import uuid
from datetime import datetime

def createChat(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chats (id, user_id, friend_id, created_at)
        VALUES (?, ?, ?, ?)
    """, (str(uuid.uuid4()), user_id, friend_id, datetime.now()))
    conn.commit()
    conn.close()

def all(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT friend_id, created_at FROM chats
        WHERE user_id = ?;
    """, (user_id,))
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects

def getFriend(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, friend_id, created_at FROM chats
        WHERE user_id = ? AND friend_id = ?;
    """, (user_id, friend_id,))
    returnedObjects = []
    for linha in cursor.fetchall():
        returnedObjects.append(linha)
    conn.close()
    return returnedObjects

def getChatWith(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, friend_id, created_at FROM chats
        WHERE user_id = ? AND friend_id = ?;
    """, (user_id, friend_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def getChatHistory(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM chats
        WHERE user_id = ? AND friend_id = ?;
    """, (user_id, friend_id,))
    chat_id = cursor.fetchone()
    if chat_id is None:
        conn.close()
        return None
    cursor.execute("""
        SELECT * FROM chat_messages
        WHERE chat_id = ?
        ORDER BY created_at ASC;
    """, (chat_id[0],))
    returnedObjects = []
    for line in cursor.fetchall():
        returnedObjects.append(line)
    conn.close()
    return returnedObjects

def getChat(chat_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM chats
        WHERE user_id = ? AND friend_id = ?;
    """, (user_id, friend_id,))
    chat_id = cursor.fetchone()
    if chat_id is None:
        conn.close()
        return None
    cursor.execute("""
        SELECT * FROM chat_messages
        WHERE chat_id = ?
        ORDER BY created_at ASC;
    """, (chat_id[0],))
    returnedObjects = []
    for line in cursor.fetchall():
        returnedObjects.append(line)
    conn.close()
    return returnedObjects

def setChatMessage(chat_id, sender_id, message):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_messages (chat_id, sender_id, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (chat_id, sender_id, message, datetime.now()))
    conn.commit()
    conn.close()
