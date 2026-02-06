# Expense Tracker

A Flask-based personal expense tracker that uses SQL Server (via `pyodbc`) for storage. Features include user registration/login, transaction recording (income/expense), budgets, savings goals, recurring transactions, receipts upload, and CSV/PDF export.

Key files:
- `my_app.py` — main Flask application and routes (DB connection in `get_connection()`).
- `conftest.py`, `test_auth.py`, `test_transactions.py` — pytest fixtures and tests.

Requirements
- Python 3.9+
- Microsoft ODBC Driver 17 for SQL Server (or appropriate driver)
- A running SQL Server instance and an `Expense_Tracker` database (or update connection string)
- Python packages: `Flask`, `Flask-Session`, `pyodbc`, `werkzeug`, `fpdf`, `pytest`

Quick setup
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or .\.venv\Scripts\activate   # cmd.exe
```

2. Install dependencies (example):

```powershell
pip install Flask Flask-Session pyodbc werkzeug fpdf pytest
```

3. Configure the database connection in `my_app.py` — update the `SERVER` and `DATABASE` values in `get_connection()` to match your SQL Server instance and credentials.

4. Ensure the required tables exist. The tests and app expect tables such as `users`, `transactions`, `categories`, `user_accounts`, `budgets`, `savings_goals`, `recurring_transactions`, etc. You can adapt your schema from the app's SQL usage.

Running the app
- With Flask (recommended):

```powershell
set FLASK_APP=my_app.py
set FLASK_ENV=development
flask run
```

Or run via Python if you add a small `if __name__ == '__main__': app.run()` block.

Tests
- Tests use `pytest`. They rely on the DB accessible from `get_connection()` and `conftest.py` rolls back changes after each test.

```powershell
pytest -q
```

Notes
- File uploads are stored under `static/receipts` (auto-created by the app). Update `ALLOWED_EXTENSIONS` in `my_app.py` if needed.
- The app uses server/trusted connection authentication in `get_connection()` — adapt to use SQL auth or environment variables for production.
- Secrets: replace `app.secret_key` with a secure secret (use environment variables in production).

Contributing
- Open issues or PRs for improvements, tests, or deployment instructions.

License
- Add a license as appropriate for your project.
# Expense-tracker