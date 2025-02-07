import sqlite3

# Conectar ao banco e listar os produtos
conn = sqlite3.connect("precos.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM produtos")
produtos = cursor.fetchall()

for produto in produtos:
    print(produto)

conn.close()
