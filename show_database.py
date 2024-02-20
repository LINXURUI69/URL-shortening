import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''select * from users''')
rows = c.fetchall()
print(rows)
conn.close()