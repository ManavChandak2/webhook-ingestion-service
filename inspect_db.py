import sqlite3

conn = sqlite3.connect("data/app.db")
cursor = conn.cursor()

print("TABLES:")
for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(row)

print("\nMESSAGES:")
for row in cursor.execute("SELECT * FROM messages;"):
    print(row)

conn.close()
