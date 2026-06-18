import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the required tables."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student'
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, email, password):
    """Create a new user. Role is always 'student' for self-registered users.
    Use make_admin.py to promote a user to admin manually."""
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
            (username, email, password_hash, 'student')
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verify a user's credentials."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

def get_user_by_id(user_id):
    """Fetch a user by their ID."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_all_users():
    """Fetch all users (Admin use)."""
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, email, role FROM users').fetchall()
    conn.close()
    return users

def delete_user(user_id):
    """Delete a user by ID (Admin use)."""
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
