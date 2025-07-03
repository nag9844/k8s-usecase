from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from prometheus_flask_exporter import PrometheusMetrics
import logging
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure value in production

# === Prometheus Metrics ===
metrics = PrometheusMetrics(app)

# === File Logger Setup ===
os.makedirs("/app/logs", exist_ok=True)
logging.basicConfig(filename='/app/logs/app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# === DB Configuration from Environment Variables ===
db_config = {
    'host': os.environ.get("DB_HOST", "localhost"),
    'user': os.environ.get("DB_USER", "root"),
    'password': os.environ.get("DB_PASSWORD", ""),
    'database': os.environ.get("DB_NAME", "testdb")
}

# === DB Initialization (Creates users table) ===
def init_db(retries=5, delay=5):
    for attempt in range(retries):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL
                )
            """)
            conn.commit()
            print("[INFO] users table created or already exists.")
            cursor.close()
            conn.close()
            return
        except mysql.connector.Error as err:
            print(f"[ERROR] DB Init failed: {err}")
            time.sleep(delay)
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            time.sleep(delay)

    print("[FATAL] Could not connect to DB after multiple retries.")
    exit(1)

# Call DB init before app starts
init_db()

# === Routes ===

@app.route('/')
def root():
    logging.info("Redirected to login page")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
            conn.commit()
            logging.info(f"User registered: {username}")
        except mysql.connector.Error as err:
            logging.error(f"Registration error: {err}")
            return f"Error: {err}"
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

        if result and check_password_hash(result[0], password):
            session['username'] = username
            logging.info(f"Login successful: {username}")
            return redirect(url_for('dashboard'))
        else:
            logging.warning(f"Login failed for user: {username}")

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        logging.info(f"Accessed dashboard: {session['username']}")
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    username = session.get('username', 'unknown')
    session.pop('username', None)
    logging.info(f"User logged out: {username}")
    return redirect(url_for('login'))

# === Prometheus endpoint is auto-mounted at /metrics ===

# === Start Server ===
if __name__ == '__main__':
    print("[INFO] Flask app starting...")
    app.run(host='0.0.0.0', port=5000)