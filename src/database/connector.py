import sqlite3

def save_to_db(df, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        price REAL,
        timestamp TEXT,
        is_weekend INTEGER
    )
    """
    cursor.execute(create_table_query)
    
    df.to_sql('user_logs', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()