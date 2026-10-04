import os
import sqlite3
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR)

# Initialize database table if it doesn't exist yet
def init_db():
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("test1.html")

@app.route("/submit", methods=["POST"])
def submit():
    complaint = request.form.get("complaint")
    location = request.form.get("location")

    # Save to SQLite database
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints (complaint, location) VALUES (?, ?)", (complaint, location))
    conn.commit()
    conn.close()

    return f"Complaint saved to database for location: {location}!"

# Route to view all saved complaints
@app.route("/admin")
def admin():
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    all_complaints = cursor.fetchall()
    conn.close()

    return f"All Saved Complaints: {all_complaints}"

if __name__ == "__main__":
    app.run(debug=True)