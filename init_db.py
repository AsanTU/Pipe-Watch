import sqlite3

def init_db():
    conn = sqlite3.connect('pipes.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pipes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        diameter TEXT,
        state TEXT,
        date_added TEXT
    );
    ''')

    cursor.execute('PRAGMA table_info(pipes);')
    columns = cursor.fetchall()
    print(columns)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()