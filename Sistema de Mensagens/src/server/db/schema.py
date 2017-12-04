import sqlite3

# conectando...
conn = sqlite3.connect('./whatsApp.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
        id CHAR(32) NOT NULL PRIMARY KEY,
        loginName VARCHAR(32) NOT NULL,
        join_at DATE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS friendship (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user CHAR(32)NOT NULL,
        friend CHAR(32) NOT NULL,
        friends_at DATE NOT NULL,
        FOREIGN KEY(user) REFERENCES users(id),
        FOREIGN KEY(friend) REFERENCES users(id)
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()
