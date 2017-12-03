import sqlite3

conn = sqlite3.connect('./db/whatsApp.db')
cursor = conn.cursor()

# lendo os dados
cursor.execute("""
SELECT * FROM users;
""")

for linha in cursor.fetchall():
    print(linha)

conn.close()
