import sqlite3


def init_db():
    conn = sqlite3.connect("downloads.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            file_path TEXT,
            file_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_download(url, title, file_path, file_type):
    conn = sqlite3.connect("downloads.db")
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO downloads (url, title, file_path, file_type) VALUES (?, ?, ?, ?)',
        (url, title, file_path, file_type)
    )
    conn.commit()
    conn.close()
