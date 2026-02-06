# test_auth.py
def test_register(client, db_cursor):
    """Test successful registration"""
    response = client.post('/register', data={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'newpass123',
        'recovery_hint': 'new hint'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    # Verify user in database
    db_cursor.execute("SELECT * FROM users WHERE email = 'new@example.com'")
    user = db_cursor.fetchone()
    assert user is not None
    assert user.full_name == 'New User'

def test_register_duplicate_email(client):
    """Test duplicate email registration"""
    # First register a user
    client.post('/register', data={
        'name': 'Duplicate',
        'email': 'duplicate@example.com',
        'password': 'testpass',
        'recovery_hint': 'hint'
    })
    
    # Try to register same email again
    response = client.post('/register', data={
        'name': 'Duplicate',
        'email': 'duplicate@example.com',
        'password': 'testpass',
        'recovery_hint': 'hint'
    }, follow_redirects=True)
    
    assert b'Email already exists' in response.data

def test_login_logout(auth_client):
    """Test login/logout functionality"""
    # Test logout
    response = auth_client.get('/logout', follow_redirects=True)
    assert b'Please log in' in response.data
    
    # Test login with invalid credentials
    response = auth_client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Invalid email or password' in response.data
    
    # Test successful login
    response = auth_client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert b'Transactions' in response.data

def test_password_recovery(client, db_cursor):
    """Test password recovery flow"""
    # Register a user first
    client.post('/register', data={
        'name': 'Recovery Test',
        'email': 'recovery@example.com',
        'password': 'oldpass',
        'recovery_hint': 'recovery hint'
    })
    
    # Test password recovery
    response = client.post('/forgot_password', data={
        'email': 'recovery@example.com',
        'hint': 'recovery hint',
        'new_password': 'newpass123'
    }, follow_redirects=True)
    
    assert b'Password reset successful' in response.data
    
    # Verify password was changed
    db_cursor.execute("SELECT password_hash FROM users WHERE email = 'recovery@example.com'")
    new_hash = db_cursor.fetchone()[0]
    assert new_hash != generate_password_hash('oldpass')