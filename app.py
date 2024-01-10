from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = "errors.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Errors (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ErrorName TEXT NOT NULL,
            Platform TEXT NOT NULL,
            FixDescription TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/add_error', methods=['POST'])
def add_error():
    error_name = request.form['error_name']
    platform = request.form['platform']
    fix_description = request.form['fix_description']

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Errors (ErrorName, Platform, FixDescription)
            VALUES (?, ?, ?)
        """, (error_name, platform, fix_description))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

    return redirect('/')

@app.route('/search_error', methods=['POST'])
def search_error():
    error_name = request.form['search_error_name']

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Use the LIKE operator for partial string matching
        cursor.execute("""
            SELECT * FROM Errors WHERE ErrorName LIKE ?
        """, ('%' + error_name + '%',))

        results = cursor.fetchall()
        conn.close()

        return render_template('search_result.html', errors=results)

    except Exception as e:
        print(f"Error: {e}")

@app.route('/list_all_errors')
def list_all_errors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Retrieve all errors from the database
        cursor.execute("SELECT * FROM Errors")
        all_errors = cursor.fetchall()

        conn.close()

        return render_template('list_all_errors.html', all_errors=all_errors)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
