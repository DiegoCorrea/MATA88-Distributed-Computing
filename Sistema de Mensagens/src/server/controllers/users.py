import sqlite3

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
