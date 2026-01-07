import sqlite3

DB_FILE = "chat_history.db"

def init_db():
    """Initialize the SQLite database and create table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_message(role, message):
    """Save a message (user or bot) to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (role, message) VALUES (?, ?)",
        (role, message)
    )
    conn.commit()
    conn.close()

def get_chat_history(limit=5):
    """Retrieve the last N messages from the database for context."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT role, message FROM chat_history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    # Return oldest first
    return rows[::-1]
