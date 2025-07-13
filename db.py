import sqlite3


DB = 'todo.db'


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            text TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            edited_by_admin BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
