import sqlite3
import os

DB_FILE = 'bookings.db'

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_bookings (
            uid TEXT PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guest_info (
            uid TEXT PRIMARY KEY,
            email TEXT,
            phone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            uid TEXT PRIMARY KEY,
            summary TEXT,
            check_in DATE,
            check_out DATE,
            pin_code TEXT,
            invoice_path TEXT,
            date_processed DATE
        )
    ''')
    conn.commit()
    conn.close()

def is_booking_processed(uid):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT uid FROM processed_bookings WHERE uid = ?', (uid,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_booking_as_processed(uid):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO processed_bookings (uid) VALUES (?)', (uid,))
    conn.commit()
    conn.close()

def add_guest_info(uid, email, phone):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO guest_info (uid, email, phone) VALUES (?, ?, ?)', (uid, email, phone))
    conn.commit()
    conn.close()

def get_guest_info(uid):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT email, phone FROM guest_info WHERE uid = ?', (uid,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {'email': result[0], 'phone': result[1]}
    else:
        return {'email': None, 'phone': None}

def add_booking(uid, summary, check_in, check_out):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO bookings (uid, summary, check_in, check_out) VALUES (?, ?, ?, ?)', (uid, summary, check_in, check_out))
    conn.commit()
    conn.close()

def update_booking_pin(uid, pin_code):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET pin_code = ? WHERE uid = ?', (pin_code, uid))
    conn.commit()
    conn.close()

def update_booking_invoice(uid, invoice_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET invoice_path = ?, date_processed = ? WHERE uid = ?', (invoice_path, datetime.now().strftime('%Y-%m-%d'), uid))
    conn.commit()
    conn.close()

def get_booking(uid):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT summary, check_in, check_out, pin_code, invoice_path, date_processed FROM bookings WHERE uid = ?', (uid,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'summary': result[0],
            'check_in': result[1],
            'check_out': result[2],
            'pin_code': result[3],
            'invoice_path': result[4],
            'date_processed': result[5]
        }
    else:
        return None

def get_all_bookings():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT uid, summary, check_in, check_out, pin_code, invoice_path, date_processed FROM bookings')
    results = cursor.fetchall()
    conn.close()
    bookings = []
    for row in results:
        bookings.append({
            'uid': row[0],
            'summary': row[1],
            'check_in': row[2],
            'check_out': row[3],
            'pin_code': row[4],
            'invoice_path': row[5],
            'date_processed': row[6]
        })
    return bookings
