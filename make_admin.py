import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def make_admin(username):
    conn = sqlite3.connect(DB_PATH)
    # Check if user exists
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if not user:
        print(f"Error: User '{username}' not found.")
        conn.close()
        return

    # Update role to admin
    conn.execute('UPDATE users SET role = "admin" WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    print(f"Success! User '{username}' is now an Admin.")

if __name__ == "__main__":
    print("=== AI Classroom Admin Promotion ===")
    username = input("Enter the username to promote to Admin: ")
    make_admin(username)
