from flask import Flask, request, render_template_string, render_template
import sqlite3

app = Flask(__name__)

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

init_db()

@app.route('/')
def home():
    return render_template('test1.html')

@app.route('/submit', methods=['POST'])
def submit():
    issue = request.form.get('issue')
    location = request.form.get('location')

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO complaints (issue, location) VALUES (?, ?)', (issue, location))
    conn.commit()
    conn.close()

    return f"<h3>Complaint registered successfully for location: {location}! <a href='/'>Submit another</a></h3>"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM complaints')
    rows = cursor.fetchall()
    conn.close()

    admin_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            body { font-family: sans-serif; background: #f8fafc; padding: 40px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
            h2 { color: #1e293b; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { text-align: left; padding: 12px; border-bottom: 1px solid #e2e8f0; }
            th { background-color: #f1f5f9; color: #475569; }
            tr:hover { background-color: #f8fafc; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Admin Complaint Dashboard</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Issue Description</th>
                    <th>Location</th>
                </tr>
                {% for row in rows %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(admin_html, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)