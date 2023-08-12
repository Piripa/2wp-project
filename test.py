import sqlite3
import pandas as pd
# conn = sqlite3.connect('frequencia.db')
# query ="SELECT name FROM sqlite_master WHERE type='table';"
# dados = pd.read_sql(query,conn)
dados = sqlite3.connect('frequencia.db')
cursor = dados.cursor()
verificar =  "SELECT name FROM sqlite_master WHERE type='table';"
lista = cursor.execute(verificar)
data = lista.fetchall()

print(data)
dados.close()
