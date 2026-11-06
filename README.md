# ExpenseAtlas
### Personal Expense Tracker & Monthly Budget Planner

ExpenseAtlas is a lightweight, self-hostable expense tracker built with Flask and SQLite. Record everyday spending, organize transactions by category, set monthly budgets, review category-wise totals, and export your records to CSV.

> **Repository description:** A Flask + SQLite personal finance app for tracking expenses, managing monthly category budgets, and exporting spending reports.

## Features
- Add expenses with title, amount, category, and date
- Browse expenses month by month
- Delete an expense when it was entered by mistake
- Create or update monthly spending limits per category
- View monthly totals and category-wise budget remaining
- Export all transactions as a CSV file
- SQLite persistence; no external database service required
- JSON API suitable for a future frontend

## Tech stack
- Python 3.10+
- Flask
- SQLite
- HTML, CSS and vanilla JavaScript
- pytest

## Project structure
```text
.
├── app.py
├── requirements.txt
├── tests/
│   └── test_app.py
├── .gitignore
├── LICENSE
└── README.md
```

## Getting started

### 1. Clone and enter the project
```bash
git clone https://github.com/kalashsri18-crypto/Kalash-1.git
cd Kalash-1
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser. The SQLite database is created automatically on startup.

### Optional configuration
Set `DATABASE` to choose a database file path. Set `FLASK_DEBUG=1` only for local development.

## API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/expenses?month=YYYY-MM` | List expenses for a month |
| POST | `/api/expenses` | Create an expense |
| DELETE | `/api/expenses/<id>` | Delete an expense |
| GET | `/api/budgets` | List category budgets |
| POST | `/api/budgets` | Create or update a category budget |
| GET | `/api/summary?month=YYYY-MM` | Monthly totals and budget status |
| GET | `/export.csv` | Download all expenses as CSV |

Example expense payload:
```json
{
  "title": "Lunch",
  "amount": 120,
  "category": "Food",
  "spent_on": "2026-11-06"
}
```

## Run tests
```bash
pytest -q
```

## Notes
This is an educational personal-finance project. It is not a banking application and does not connect to bank accounts. Keep the database file private and back it up regularly.

## License
See [LICENSE](LICENSE).
