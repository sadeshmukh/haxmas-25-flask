import flask
import sqlite3
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = flask.Flask(__name__, static_folder="static", static_url_path="/")


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)

DB_PATH = os.getenv("DB_PATH", "wishes.db")
conn = sqlite3.connect(os.getenv("DB_PATH", "wishes.db"))
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS wishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        wish TEXT NOT NULL,
        color TEXT NOT NULL
    )
"""
)
conn.commit()
conn.close()


@app.get("/")
@limiter.exempt
def index():
    return flask.send_from_directory("static", "index.html")


@app.post("/wishes")
@limiter.limit("10 per day")
def make_a_wish():
    data = flask.request.get_json()
    name = data.get("name")
    wish = data.get("wish")
    color = data.get("color")

    if not name or not wish or not color:
        return "Name, wish, and color are required"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO wishes (name, wish, color) VALUES (?, ?, ?)", (name, wish, color)
    )
    conn.commit()
    conn.close()
    return "Wish added", 201


@app.get("/wishes")
@limiter.exempt
def get_wishes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, wish, color FROM wishes")
    rows = cursor.fetchall()
    conn.close()

    wishes = [
        {"id": row[0], "name": row[1], "wish": row[2], "color": row[3]} for row in rows
    ]
    return flask.jsonify(wishes)


if __name__ == "__main__":
    app.run()
