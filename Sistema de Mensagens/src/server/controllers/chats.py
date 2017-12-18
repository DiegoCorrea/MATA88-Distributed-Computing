import sqlite3
import uuid
from datetime import datetime
from time import gmtime, strftime

def createChat(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chats (id, user_id, friend_id, created_at)
        VALUES (?, ?, ?, ?)
    """, (str(uuid.uuid4()), user_id, friend_id, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    conn.commit()
    conn.close()

def allUserChat(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, friend_id, created_at FROM chats
        WHERE user_id = ? OR friend_id = ?;
    """, (user_id, user_id,))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data

def getChatWith(user_id, friend_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, friend_id, created_at FROM chats
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?);
    """, (user_id, friend_id, friend_id, user_id,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data

def getChatMessages(chat_id, limit=20):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM chat_messages
        WHERE chat_id = ?
        ORDER BY date(created_at) DESC Limit ?;
    """, (chat_id, limit))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data

def setChatMessage(chat_id, sender_id, message):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_messages (chat_id, sender_id, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (chat_id, sender_id, message, str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))))
    conn.commit()
    conn.close()
