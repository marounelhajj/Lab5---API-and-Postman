import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("SELECT * FROM users")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
