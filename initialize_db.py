import sqlite3

DB_NAME = 'example.db'

# Connect to database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create tables (custom account_number)
cursor.execute('''
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT UNIQUE,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    balance REAL DEFAULT 0.0
)
''')

cursor.execute('''
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    type TEXT,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()