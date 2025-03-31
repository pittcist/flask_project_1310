import sqlite3 as sql

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, zip TEXT)')
print("Table created successfully")

conn.close()