# conftest.py
import pytest
import pytest
import os
import sys
import sqlite3
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_app import app as flask_app, get_connection
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SESSION_TYPE'] = 'filesystem'
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def _init_sqlite_schema(conn):
    c = conn.cursor()
    # Minimal tables required for tests
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            recovery_hint TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            account_name TEXT,
            account_type TEXT,
            current_balance REAL DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT,
            category_type TEXT,
            user_id INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_id INTEGER,
            amount REAL,
            transaction_type TEXT,
            transaction_date TEXT,
            description TEXT,
            receipt_url TEXT,
            account_id INTEGER
        )
    ''')
    conn.commit()


@pytest.fixture
def db_cursor():
    # Provide a DB cursor for tests. If using sqlite (DB_ENGINE=sqlite),
    # create an in-memory DB and initialize schema for isolation.
    engine = os.getenv('DB_ENGINE', 'mssql').lower()

    if engine == 'sqlite':
        db_path = os.getenv('DB_PATH', ':memory:')
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        _init_sqlite_schema(conn)
        cursor = conn.cursor()
        yield cursor
        conn.close()
    else:
        conn = get_connection()
        cursor = conn.cursor()
        yield cursor
        try:
            conn.rollback()
        finally:
            conn.close()


@pytest.fixture
def auth_client(client, db_cursor):
    # Register test user
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass123',
        'recovery_hint': 'test hint'
    })

    # Login
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })

    yield client

    # Cleanup (best-effort)
    try:
        db_cursor.execute("DELETE FROM users WHERE email = 'test@example.com'")
    except Exception:
        pass