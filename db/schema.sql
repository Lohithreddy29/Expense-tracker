-- SQL Server schema for Expense Tracker (create in your Expense_Tracker database)

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users]') AND type in (N'U'))
BEGIN
    CREATE TABLE users (
        user_id INT IDENTITY(1,1) PRIMARY KEY,
        full_name NVARCHAR(255) NOT NULL,
        email NVARCHAR(255) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        recovery_hint NVARCHAR(255) NULL
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user_accounts]') AND type in (N'U'))
BEGIN
    CREATE TABLE user_accounts (
        account_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        account_name NVARCHAR(255) NOT NULL,
        account_type NVARCHAR(100) NULL,
        current_balance DECIMAL(18,2) NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[categories]') AND type in (N'U'))
BEGIN
    CREATE TABLE categories (
        category_id INT IDENTITY(1,1) PRIMARY KEY,
        category_name NVARCHAR(255) NOT NULL,
        category_type NVARCHAR(50) NOT NULL,
        user_id INT NULL -- NULL for global categories
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[transactions]') AND type in (N'U'))
BEGIN
    CREATE TABLE transactions (
        transaction_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        category_id INT NULL,
        amount DECIMAL(18,2) NOT NULL,
        transaction_type NVARCHAR(20) NOT NULL,
        transaction_date DATETIME NOT NULL,
        description NVARCHAR(1024) NULL,
        receipt_url NVARCHAR(1024) NULL,
        account_id INT NULL,
        is_recurring_generated BIT NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[budgets]') AND type in (N'U'))
BEGIN
    CREATE TABLE budgets (
        budget_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        category_id INT NOT NULL,
        budget_amount DECIMAL(18,2) NOT NULL,
        budget_month DATE NOT NULL,
        alert_threshold INT NOT NULL DEFAULT 90
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[savings_goals]') AND type in (N'U'))
BEGIN
    CREATE TABLE savings_goals (
        goal_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        goal_name NVARCHAR(255) NOT NULL,
        target_amount DECIMAL(18,2) NOT NULL,
        current_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
        target_date DATE NULL
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[savings_history]') AND type in (N'U'))
BEGIN
    CREATE TABLE savings_history (
        history_id INT IDENTITY(1,1) PRIMARY KEY,
        goal_id INT NOT NULL,
        amount DECIMAL(18,2) NOT NULL,
        contribution_date DATETIME NOT NULL,
        FOREIGN KEY (goal_id) REFERENCES savings_goals(goal_id)
    );
END

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[recurring_transactions]') AND type in (N'U'))
BEGIN
    CREATE TABLE recurring_transactions (
        recurring_id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        category_id INT NOT NULL,
        account_id INT NULL,
        amount DECIMAL(18,2) NOT NULL,
        transaction_type NVARCHAR(20) NOT NULL,
        frequency NVARCHAR(20) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NULL,
        description NVARCHAR(1024) NULL,
        last_generated_date DATE NULL,
        is_active BIT NOT NULL DEFAULT 1
    );
END
