import os
import sqlite3
from code.db_handler import init_db


def test_init_db():
    init_db()
    assert os.path.exists("downloads.db")
    conn = sqlite3.connect("downloads.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
        " AND name='downloads'"
    )
    assert cursor.fetchone() is not None
