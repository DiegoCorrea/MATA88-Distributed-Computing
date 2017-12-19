import sqlite3, uuid
from time import gmtime, strftime

def createGroup(group_name):
    group_id = str(uuid.uuid4())[:8]
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO groups (id, name, created_at)
        VALUES (?, ?, ?)
    """, (group_id, group_name, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    conn.commit()
    conn.close()
    return group_id

def allUsers(group_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users_groups
        WHERE group_id = ?;
    """, (group_id,))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data

def userGroups(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users_groups
        WHERE user_id = ?;
    """, (user_id,))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data

def addUser(user_id, group_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users_groups (user_id, group_id, created_at)
        VALUES (?, ?, ?)
    """, (user_id, group_id, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    conn.commit()
    conn.close()

def findBy_ID(group_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM groups
        WHERE id = ?;
    """, (group_id,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data
