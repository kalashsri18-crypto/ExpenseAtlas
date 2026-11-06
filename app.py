import os, sqlite3, csv, io
from datetime import date
from flask import Flask, request, jsonify, render_template_string, Response

app = Flask(__name__)
app.config["DATABASE"] = os.environ.get("DATABASE", "expenseatlas.sqlite3")

def db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY, title TEXT NOT NULL, amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL, spent_on TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS budgets(
            category TEXT PRIMARY KEY, monthly_limit REAL NOT NULL CHECK(monthly_limit > 0))""")

@app.get("/api/expenses")
def expenses():
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    with db() as c:
        rows = c.execute("SELECT * FROM expenses WHERE substr(spent_on,1,7)=? ORDER BY spent_on DESC,id DESC",(month,)).fetchall()
    return jsonify([dict(x) for x in rows])

@app.post("/api/expenses")
def add_expense():
    d = request.get_json(silent=True) or request.form
    try:
        title, category = str(d.get("title","")).strip(), str(d.get("category","")).strip()
        amount, spent_on = float(d.get("amount",0)), str(d.get("spent_on",date.today().isoformat()))
        date.fromisoformat(spent_on)
        if not title or not category or amount <= 0: raise ValueError()
    except (ValueError, TypeError):
        return jsonify(error="Enter a title, category, positive amount and valid date."),400
    with db() as c:
        cur=c.execute("INSERT INTO expenses(title,amount,category,spent_on) VALUES(?,?,?,?)",(title,amount,category,spent_on))
        row=c.execute("SELECT * FROM expenses WHERE id=?",(cur.lastrowid,)).fetchone()
    return jsonify(dict(row)),201

@app.delete("/api/expenses/<int:item_id>")
def delete_expense(item_id):
    with db() as c: cur=c.execute("DELETE FROM expenses WHERE id=?",(item_id,))
    return ("",204) if cur.rowcount else (jsonify(error="Expense not found"),404)

@app.route("/api/budgets",methods=["GET","POST"])
def budgets():
    if request.method=="POST":
        d=request.get_json(silent=True) or request.form
        try:
            category=str(d.get("category","")).strip(); limit=float(d.get("monthly_limit",0))
            if not category or limit<=0: raise ValueError()
        except (ValueError,TypeError): return jsonify(error="Category and positive monthly limit required."),400
        with db() as c: c.execute("INSERT INTO budgets VALUES(?,?) ON CONFLICT(category) DO UPDATE SET monthly_limit=excluded.monthly_limit",(category,limit))
    with db() as c: rows=c.execute("SELECT * FROM budgets ORDER BY category").fetchall()
    return jsonify([dict(x) for x in rows])

@app.get("/api/summary")
def summary():
    month=request.args.get("month",date.today().strftime("%Y-%m"))
    with db() as c:
        spent=c.execute("SELECT category,SUM(amount) total FROM expenses WHERE substr(spent_on,1,7)=? GROUP BY category",(month,)).fetchall()
        limits={r["category"]:r["monthly_limit"] for r in c.execute("SELECT * FROM budgets")}
    return jsonify(month=month,categories=[dict(category=r["category"],spent=r["total"],budget=limits.get(r["category"]),remaining=(limits[r["category"]]-r["total"]) if r["category"] in limits else None) for r in spent],total=round(sum(r["total"] for r in spent),2))

@app.get("/export.csv")
def export_csv():
    with db() as c: rows=c.execute("SELECT title,amount,category,spent_on FROM expenses ORDER BY spent_on DESC").fetchall()
    out=io.StringIO(); w=csv.writer(out); w.writerow(["title","amount","category","spent_on"])
    w.writerows([tuple(r) for r in rows])
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=expenses.csv"})

@app.get("/")
def home():
    return render_template_string("""<!doctype html><title>ExpenseAtlas</title><meta name=viewport content="width=device-width,initial-scale=1"><style>
    body{font:16px system-ui;max-width:850px;margin:3rem auto;padding:0 1rem;background:#f5f7fb;color:#182238}main{background:white;padding:2rem;border-radius:16px;box-shadow:0 5px 25px #18223812}form{display:flex;gap:.6rem;flex-wrap:wrap}input,button{padding:.7rem;border:1px solid #ccd3df;border-radius:8px}button{background:#234c8a;color:white;cursor:pointer}li{padding:.5rem;border-bottom:1px solid #eee}.muted{color:#65718a}</style><main><h1>ExpenseAtlas</h1><p class=muted>Track spending, budgets and monthly trends.</p><form id=f><input name=title placeholder="Expense" required><input name=amount type=number step=.01 min=.01 placeholder="Amount" required><input name=category placeholder="Category" required><input name=spent_on type=date><button>Add expense</button></form><h2 id=total></h2><ul id=list></ul><p><a href=/export.csv>Export all expenses as CSV</a></p></main><script>
    async function load(){let r=await fetch('/api/expenses');let a=await r.json();list.innerHTML=a.map(x=>'<li>'+x.spent_on+' · '+x.title+' · '+x.category+' — ₹'+x.amount.toFixed(2)+' <button onclick="del('+x.id+')">Delete</button></li>').join('');let s=await (await fetch('/api/summary')).json();total.textContent='This month: ₹'+s.total.toFixed(2)}
    f.onsubmit=async e=>{e.preventDefault();let d=Object.fromEntries(new FormData(f));let r=await fetch('/api/expenses',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});if(!r.ok){alert((await r.json()).error);return}f.reset();load()};
    async function del(id){await fetch('/api/expenses/'+id,{method:'DELETE'});load()}load();</script>""")

if __name__=="__main__":
    init_db(); app.run(debug=os.environ.get("FLASK_DEBUG")=="1")
else:
    with app.app_context(): init_db()
