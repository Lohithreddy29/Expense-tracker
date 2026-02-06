# conftest.py
import pytest
import os
import sys
from my_app import app as flask_app, get_connection
from werkzeug.security import generate_password_hash

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SESSION_TYPE'] = 'filesystem'
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    yield cursor
    conn.rollback()  # Rollback after each test
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
    
    # Cleanup
    db_cursor.execute("DELETE FROM users WHERE email = 'test@example.com'")