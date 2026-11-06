from app import app, init_db
import pytest

@pytest.fixture
def client(tmp_path):
    app.config["TESTING"]=True
    app.config["DATABASE"]=str(tmp_path/"test.sqlite3")
    init_db()
    return app.test_client()

def test_add_and_list_expense(client):
    r=client.post("/api/expenses",json={"title":"Lunch","amount":120,"category":"Food","spent_on":"2026-11-06"})
    assert r.status_code==201
    assert client.get("/api/expenses?month=2026-11").json[0]["title"]=="Lunch"

def test_reject_invalid_expense(client):
    assert client.post("/api/expenses",json={"title":"","amount":-1}).status_code==400

def test_budget_summary(client):
    client.post("/api/budgets",json={"category":"Food","monthly_limit":1000})
    client.post("/api/expenses",json={"title":"Meal","amount":100,"category":"Food","spent_on":"2026-11-06"})
    assert client.get("/api/summary?month=2026-11").json["total"]==100
