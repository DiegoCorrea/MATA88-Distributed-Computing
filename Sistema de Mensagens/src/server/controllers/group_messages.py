import sqlite3
import uuid
from datetime import datetime
from time import gmtime, strftime

def getMessages(group_id, limit=20):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM group_messages
        WHERE group_id = ?
        ORDER BY date(created_at) DESC Limit ?;
    """, (group_id, limit))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data

def sendMessage(group_id, sender_id, message):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO group_messages (group_id, sender_id, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (group_id, sender_id, message, str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))))
    conn.commit()
    conn.close()
