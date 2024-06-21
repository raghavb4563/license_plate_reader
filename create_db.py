import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS registered_vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE,
        owner_name TEXT
    )
    ''')
    # c.execute('''
    # CREATE TABLE IF NOT EXISTS access_logs (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     plate_number TEXT,
    #     timestamp TEXT
    # )
    # ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT,
        owner_name TEXT,
        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
