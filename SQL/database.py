import sqlite3

DB_NAME = "jobs.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company TEXT,
            location TEXT,
            salary TEXT,
            posted_date TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_jobs(df):
    conn = create_connection()
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
