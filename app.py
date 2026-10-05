from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database and ensure correct table schema exists
def init_db():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run database setup on server startup
init_db()

# 1. Main Home Page Route (Shows Complaint Submission Form)
@app.route('/')
def home():
    return render_template('index.html')

# 2. Form Submission Route
@app.route('/submit', methods=['POST'])
def submit():
    issue = request.form.get('issue')
    location = request.form.get('location')

    if issue and location:
        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO complaints (issue, location) VALUES (?, ?)',
            (issue, location)
        )
        conn.commit()
        conn.close()

    # Redirect to admin dashboard after successful submission
    return redirect(url_for('admin'))

# 3. Admin Dashboard Route (Styled Dark-Mode View)
@app.route('/admin')
def admin():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM complaints ORDER BY id DESC')
    data = cursor.fetchall()
    conn.close()

    rows = ""
    if data:
        for row in data:
            rows += f"<tr><td>#{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    else:
        rows = '<tr><td colspan="3" style="text-align: center; color: #64748b;">No complaints logged yet.</td></tr>'

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard - CampusFix</title>
        <link rel="stylesheet" href="/static/style.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="page-wrapper">
            <header class="navbar">
                <div class="logo">⚡ Campus<span>Fix</span></div>
                <a href="/" class="nav-link">← Back to Form</a>
            </header>

            <main class="content-container">
                <div class="table-card">
                    <div class="card-header">
                        <h2>Submitted Complaints</h2>
                        <p>Live administrative view of all student infrastructure tickets.</p>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Ticket ID</th>
                                <th>Issue Description</th>
                                <th>Location</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True)