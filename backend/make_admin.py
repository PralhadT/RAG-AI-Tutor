import sqlite3
import os
import sys

# database.db is one directory up from the backend folder
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def make_admin(username):
    conn = sqlite3.connect(DB_PATH)
    # Check if user exists
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if not user:
        print(f"Error: User '{username}' not found in the database.")
        conn.close()
        return

    # Update role to admin
    conn.execute('UPDATE users SET role = "admin" WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    print(f"Success! User '{username}' has been promoted to Admin.")

if __name__ == "__main__":
    print("=== AI Classroom Admin Promotion ===")
    
    # If the user provided the username in the command (e.g. python make_admin.py prash)
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter the username to promote to Admin: ")
        
    make_admin(username)
