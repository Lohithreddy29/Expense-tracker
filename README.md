# Expense Tracker

A Flask-based personal expense tracker with features including user registration/login, transaction recording (income/expense), budgets, savings goals, recurring transactions, receipt uploads, and CSV/PDF export.

Key files
- `my_app.py` — main Flask application and routes (DB connection via environment variables).
- `db/schema.sql` — starter SQL Server schema.
- `scripts/init_db.py` — helper to apply `db/schema.sql` to a SQL Server instance.
- Tests: `conftest.py`, `test_auth.py`, `test_transactions.py` (pytest).

Requirements
- Python 3.9+
- For production with SQL Server: Microsoft ODBC Driver 17 for SQL Server (or appropriate driver)
- A SQL Server instance for production (or use Docker compose locally)

Files for dependency management
- `requirements.txt` — lightweight list used for local installs.
- `requirements-pinned.txt` — recommended pinned versions.
- `requirements-ci.txt` — CI/test dependencies (excludes `pyodbc` so tests run in CI using SQLite).

Quick setup (local, Python)
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or .\.venv\Scripts\activate   # cmd.exe
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values (DB connection, `APP_SECRET`, etc.).

4. If using SQL Server, initialize the DB schema:

```powershell
python scripts/init_db.py
```

Running the app
- With Flask (development):

```powershell
set FLASK_APP=my_app.py
set FLASK_ENV=development
flask run
```

Or build and run with Docker:

```powershell
docker-compose up --build
```

Testing
- The test suite uses an in-memory SQLite database in CI and can be run locally in the same mode. To run tests locally with SQLite:

```powershell
set DB_ENGINE=sqlite
set DB_PATH=:memory:
pytest -q
```

CI
- GitHub Actions is configured in `.github/workflows/ci.yml`. The workflow runs linting and tests. Tests are enabled and run against an in-memory SQLite DB so no external DB is required.

Pinning
- `requirements-pinned.txt` contains suggested pinned versions. To produce an exact freeze from your environment run:

```powershell
pip freeze > requirements.txt
```

Notes & Security
- Store secrets in `.env` (don't commit it). Use `APP_SECRET` for `app.secret_key` and `DB_*` variables for DB configuration.
- For production, do not use the development server and ensure strong secrets and secure DB credentials.

License & Contributing
- See `LICENSE` (MIT) and `CONTRIBUTING.md` for contribution guidelines.
