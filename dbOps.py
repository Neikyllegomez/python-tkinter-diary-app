import sqlite3

# Function to create a database and table if they don't exist
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Function to register a user
def register_user(first_name, last_name, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, password))
        conn.commit()
        return True  # Return True on success
    except sqlite3.IntegrityError:
        return False  # Return False if email already exists
    finally:
        conn.close()

# Function to login a user
def login_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email=? AND password=?
    ''', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Return user object or None if not found

# Function to add a new diary entry
def add_diary_entry(title, content, user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diary (title, content, user_id)
        VALUES (?, ?, ?)
    ''', (title, content, user_id))
    conn.commit()
    conn.close()

# Function to fetch all diary entries for a user
def fetch_diary_entries(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM diary WHERE user_id=?', (user_id,))
    entries = cursor.fetchall()
    conn.close()
    return entries

# Function to update a diary entry
def update_diary_entry(entry_id, title, content):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE diary SET title=?, content=?
        WHERE id=?
    ''', (title, content, entry_id))
    conn.commit()
    conn.close()

# Function to delete a diary entry
def delete_diary_entry(entry_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM diary WHERE id=?', (entry_id,))
    conn.commit()
    conn.close()
