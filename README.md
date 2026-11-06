# ExpenseAtlas

ExpenseAtlas is a focused, self-hostable application for a practical everyday workflow.

## Features

- Record and delete expenses with validated amount, category and date
- Set per-category monthly budgets and inspect remaining budget
- View month/category totals and export CSV

## Stack

Python 3.10+, Flask, SQLite, HTML/CSS/vanilla JavaScript, pytest.

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Tests

```bash
pytest
```

Set `DATABASE` to choose a SQLite file path. The default database is created automatically. No paid API or external service is required.

## API

JSON endpoints are documented by their route names in `app.py`. Invalid input returns a JSON error and appropriate HTTP status code.

## License

MIT. See [LICENSE](LICENSE).
