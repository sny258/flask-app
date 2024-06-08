from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()

            if user:
                cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cur.fetchone()
                if user:
                    session['username'] = username
                    return redirect(url_for('welcome'))
                else:
                    flash('Invalid username or password. Please try again.')
            else:
                flash('User does not exist. Please sign up.')

    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user:
            flash('Username already exists. Please choose a different one.')
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            session['username'] = username
            return redirect(url_for('welcome'))

    return redirect(url_for('login'))


@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


#routes for itenary
@app.route('/leh_itinerary')
def leh_itinerary():
    if 'username' in session:
        return render_template('leh_itinerary.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
@app.route('/kedarnath_itinerary')
def kedarnath_itinerary():
    if 'username' in session:
        return render_template('kedarnath_itinerary.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
@app.route('/manali_itinerary')
def manali_itinerary():
    if 'username' in session:
        return render_template('manali_itinerary.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
