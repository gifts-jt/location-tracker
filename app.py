from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "locations.db"


# -----------------------------
# Create Database
# -----------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            accuracy REAL,
            ip_address TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# Initialize database
init_db()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Save Location
# -----------------------------
@app.route("/save_location", methods=["POST"])
def save_location():

    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    accuracy = data.get("accuracy")

    ip = request.remote_addr

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO locations
        (latitude, longitude, accuracy, ip_address, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        latitude,
        longitude,
        accuracy,
        ip,
        current_time
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Location Saved Successfully"
    })


# -----------------------------
# Admin Dashboard
# -----------------------------
@app.route("/admin")
def admin():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM locations
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template("admin.html", rows=rows)


# -----------------------------
# API
# -----------------------------
@app.route("/api/locations")
def api_locations():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM locations
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)