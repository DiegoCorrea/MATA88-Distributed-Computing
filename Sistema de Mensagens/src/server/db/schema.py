import sqlite3
import os
import inspect
# conectando...
conn = sqlite3.connect(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/whatsApp.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
print('Users')
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
        id CHAR(32) NOT NULL PRIMARY KEY,
        name VARCHAR(32) NOT NULL,
        email VARCHAR(32) NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
);
""")
print('...Ok!')
print('Friendship')
cursor.execute("""
CREATE TABLE IF NOT EXISTS friendships (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(32) NOT NULL,
        friend_id CHAR(32) NOT NULL,
        created_at DATE NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(friend_id) REFERENCES users(id)
);
""")
print('...Ok!')
print('User Message')
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_messages (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        sender_id CHAR(32) NOT NULL,
        message TEXT NOT NULL,
        message_time TEXT NOT NULL,
        FOREIGN KEY(sender_id) REFERENCES friendship(id)
);
""")
print('...Ok!')
print('Groups ')
cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
        id CHAR(32) NOT NULL PRIMARY KEY,
        name CHAR(32) NOT NULL
);
""")
print('...Ok!')

print('Users Groups ')
cursor.execute("""
CREATE TABLE IF NOT EXISTS users_groups (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(32)NOT NULL,
        group_id CHAR(32) NOT NULL,
        created_at DATE NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(group_id) REFERENCES groups(id)
);
""")
print('...OK!')
print('Group Messages')
cursor.execute("""
CREATE TABLE IF NOT EXISTS group_messages (
        id CHAR(32) NOT NULL PRIMARY KEY,
        user_id CHAR(32) NOT NULL,
        group_id CHAR(32) NOT NULL,
        created_at TEXT NOT NULL,
        message TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(group_id) REFERENCES groups(id)
);
""")
print('...OK!')
print('Tabelas criadas com sucesso.')
# desconectando...
conn.close()
