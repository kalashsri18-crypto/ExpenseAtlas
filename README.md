<div align="center">

# 💸 ExpenseAtlas

### Personal Expense Tracker & Monthly Budget Planner

Track your spending, manage category budgets, and understand where your money goes.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-See%20LICENSE-lightgrey?style=for-the-badge)

</div>

---

## 📌 Overview

**ExpenseAtlas** is a lightweight, self-hostable personal finance application built with Flask and SQLite. It helps you record everyday expenses, organize transactions by category, set monthly budgets, review spending summaries, and export your records to CSV.

## ✨ Features

- 🧾 **Expense tracking** — add, view, and delete transactions
- 🗂️ **Category management** — organize spending by category
- 🎯 **Monthly budgets** — create or update category-wise limits
- 📊 **Spending summary** — view monthly totals and remaining budget
- 📥 **CSV export** — download transaction records
- 💾 **Local database** — SQLite storage with no external database service
- 🔌 **JSON API** — endpoints ready for a future frontend

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| Flask | Backend web framework |
| SQLite | Data storage |
| HTML, CSS, JavaScript | Frontend |
| pytest | Automated testing |

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or later
- pip

### Installation

```bash
git clone https://github.com/kalashsri18-crypto/ExpenseAtlas.git
cd ExpenseAtlas

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser. The SQLite database is created automatically on startup.

### Configuration

- Set `DATABASE` to use a custom SQLite database path.
- Set `FLASK_DEBUG=1` only during local development.

## 🔗 API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/expenses?month=YYYY-MM` | List expenses for a month |
| POST | `/api/expenses` | Create an expense |
| DELETE | `/api/expenses/<id>` | Delete an expense |
| GET | `/api/budgets` | List category budgets |
| POST | `/api/budgets` | Create or update a category budget |
| GET | `/api/summary?month=YYYY-MM` | Monthly totals and budget status |
| GET | `/export.csv` | Export expenses as CSV |

Example request body:

```json
{
  "title": "Lunch",
  "amount": 120,
  "category": "Food",
  "spent_on": "2026-11-06"
}
```

## 🧪 Run Tests

```bash
pytest -q
```

## 📁 Project Structure

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

## 🔒 Note

ExpenseAtlas is an educational personal-finance project. It is not a banking application and does not connect to bank accounts. Keep your local database private and back it up regularly.

## 👨‍💻 Author

**Kalash Srivastava**  
[GitHub](https://github.com/kalashsri18-crypto) · [LinkedIn](https://www.linkedin.com/in/kalash-srivastava-b6592a3b3) · [Email](mailto:kalashsri18@gmail.com)

---

<div align="center">
  Made with ❤️ by Kalash
</div>
