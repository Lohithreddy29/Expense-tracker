"""Initialize database using `db/schema.sql` for SQL Server.

Usage:
  python scripts/init_db.py

Reads DB connection from env vars (see README or .env.example).
"""
import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

def main():
    conn_str = os.getenv('DB_CONNECTION')
    if not conn_str:
        driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_DATABASE')
        trusted = os.getenv('DB_TRUSTED', 'yes').lower() in ('yes','true','1')
        if trusted:
            conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        else:
            user = os.getenv('DB_USER')
            password = os.getenv('DB_PASSWORD')
            conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}"

    if not conn_str:
        print('No DB connection configured in environment.')
        return

    sql_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')
    with open(sql_path, 'r', encoding='utf-8') as fh:
        sql = fh.read()

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        print('Schema applied successfully.')
    finally:
        conn.close()

if __name__ == '__main__':
    main()
