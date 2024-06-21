import sqlite3
from datetime import datetime


def add_registered_vehicle(plate_number, owner_name):
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    c.execute('INSERT INTO registered_vehicles (plate_number, owner_name) VALUES (?, ?)', (plate_number, owner_name))
    conn.commit()
    conn.close()
    print("hello")

def check_registered_vehicle(plate_number):
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    c.execute('SELECT owner_name FROM registered_vehicles WHERE plate_number = ?', (plate_number,))
    result = c.fetchone()
    conn.close()
    return result

def log_access(plate_number,owner):
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO logs (plate_number, owner_name, timestamp) VALUES (?, ?, ?)', (plate_number, owner, timestamp))
    conn.commit()
    conn.close()

def get_access_logs():
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    c.execute('SELECT plate_number, owner_name, timestamp FROM logs')
    logs = c.fetchall()
    conn.close()
    return logs

def del_logs():
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    c.execute('Delete from logs')
    conn.commit()
    conn.close()
    

def get_registered_vehicles():
    conn = sqlite3.connect('vehicle_db.sqlite')
    c = conn.cursor()
    c.execute('SELECT plate_number, owner_name FROM registered_vehicles')
    logs = c.fetchall()
    conn.close()
    return logs

