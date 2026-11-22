
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to database
def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

# Home page
@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()

    if title:
        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        conn.commit()
        conn.close()

    return redirect("/")

# Complete task
@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()
    return redirect("/")

# Delete task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
