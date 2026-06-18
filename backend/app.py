import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

from flask import Flask, render_template, session, redirect, url_for, flash  # flash added
from routes.auth_routes import auth_bp
from routes.upload_routes import upload_bp
from routes.chat_routes import chat_bp
from models.user_model import init_db

app = Flask(__name__)

# Basic configuration
app.secret_key = os.environ.get('SECRET_KEY', 'super-secret-development-key')

# Optional: ensure API key is available (debug helper)
if not os.environ.get("GOOGLE_API_KEY"):
    print("WARNING: GOOGLE_API_KEY is not set!")

# Initialize the database
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(chat_bp, url_prefix='/chat')

@app.route('/')
def home():
    """Home page."""
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    """User dashboard."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = str(session.get('user_id'))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')

    # Get files uploaded by this user
    user_files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith(user_id + '_'):
                display_name = filename[len(user_id) + 1:]
                user_files.append(display_name)

    return render_template('dashboard.html', files=user_files)

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to manage users and global files."""
    if session.get('role') != 'admin':
        flash('Unauthorized Access! Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))

    from models.user_model import get_all_users
    users = get_all_users()

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    all_files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            parts = filename.split('_', 1)
            if len(parts) == 2:
                owner_id = parts[0]
                display_name = parts[1]
                all_files.append({
                    'raw_filename': filename,
                    'display_name': display_name,
                    'owner_id': owner_id
                })

    return render_template('admin_dashboard.html', users=users, files=all_files)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    from models.user_model import delete_user
    delete_user(user_id)
    flash(f'User ID {user_id} has been deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_file/<filename>', methods=['POST'])
def admin_delete_file(filename):
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'File {filename} deleted globally.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
