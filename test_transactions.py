def test_add_transaction(auth_client, db_cursor):
    # First add a category and account
    db_cursor.execute("""
        INSERT INTO categories (category_name, category_type, user_id)
        VALUES ('Test Category', 'expense', 1)
    """)
    db_cursor.execute("""
        INSERT INTO user_accounts (account_name, account_type, user_id, current_balance)
        VALUES ('Test Account', 'Checking', 1, 1000)
    """)
    
    # Test adding income transaction
    response = auth_client.post('/add_transaction', data={
        'category_id': 1,
        'transaction_type': 'income',
        'amount': 500,
        'transaction_date': '2023-01-01',
        'account_id': 1
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Transactions' in response.data
    
    # Verify transaction in database
    db_cursor.execute("SELECT * FROM transactions WHERE user_id = 1")
    transactions = db_cursor.fetchall()
    assert len(transactions) == 1
    assert transactions[0].amount == 500
    
    # Verify account balance updated
    db_cursor.execute("SELECT current_balance FROM user_accounts WHERE account_id = 1")
    balance = db_cursor.fetchone()[0]
    assert balance == 1500

def test_edit_transaction(auth_client, db_cursor):
    # Add test transaction
    db_cursor.execute("""
        INSERT INTO transactions (user_id, category_id, amount, transaction_type, 
                                transaction_date, account_id)
        VALUES (1, 1, 100, 'expense', '2023-01-01', 1)
    """)
    
    # Edit the transaction
    response = auth_client.post('/edit_transaction/1', data={
        'category_id': 1,
        'transaction_type': 'expense',
        'amount': 150,
        'transaction_date': '2023-01-01',
        'account_id': 1
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify changes
    db_cursor.execute("SELECT amount FROM transactions WHERE transaction_id = 1")
    assert db_cursor.fetchone()[0] == 150
    
    # Verify account balance adjusted correctly (100 -> 150 expense)
    db_cursor.execute("SELECT current_balance FROM user_accounts WHERE account_id = 1")
    assert db_cursor.fetchone()[0] == 1350

def test_delete_transaction(auth_client, db_cursor):
    # Add test transaction
    db_cursor.execute("""
        INSERT INTO transactions (user_id, category_id, amount, transaction_type, 
                                transaction_date, account_id)
        VALUES (1, 1, 200, 'expense', '2023-01-01', 1)
    """)
    
    # Delete the transaction
    response = auth_client.get('/delete_transaction/1', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify deletion
    db_cursor.execute("SELECT COUNT(*) FROM transactions WHERE transaction_id = 1")
    assert db_cursor.fetchone()[0] == 0
    
    # Verify account balance adjusted
    db_cursor.execute("SELECT current_balance FROM user_accounts WHERE account_id = 1")
    assert db_cursor.fetchone()[0] == 1500