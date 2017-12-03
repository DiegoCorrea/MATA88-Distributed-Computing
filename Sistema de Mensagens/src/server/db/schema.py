import sqlite3

# conectando...
conn = sqlite3.connect('./whatsApp.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE users (
        id CHAR(32) NOT NULL PRIMARY KEY,
        loginName VARCHAR(32) NOT NULL,
        join_at DATE NOT NULL
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()