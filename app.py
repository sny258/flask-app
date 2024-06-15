from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    
    # Create a cursor using conn for executing SQL queries 
    cur = conn.cursor()
    # Check if users table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cur.fetchone():
        print("users table already exists")
    else:
        # Create users table
        #cur.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)')
        cur.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, first_name TEXT, last_name TEXT, email TEXT, security_question TEXT, security_answer TEXT);')
        print("users table created successfully")
    # Check if bookings table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
    if cur.fetchone():
        print("bookings table already exists")
    else:
        # Create bookings table, booking_id is the primary key and it auto increments
        cur.execute('CREATE TABLE bookings (booking_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, name TEXT, email TEXT, phone TEXT, trip TEXT, date TEXT)')
        print("bookings table created successfully")

    #close the connection
    conn.close()

init_sqlite_db()

# Home page route, which redirects to login page
@app.route('/')
def home():
    return redirect(url_for('login'))

# login page route, which will accept both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Connect to DB and create a cursor
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()
            # Check if user exists in DB, otherwise need to Sign up  
            if user:
                # Check if username and password combination exists, then redirect to welcome page
                # Otherwise Invalida username or password.
                cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cur.fetchone()
                if user:
                    session['username'] = username
                    return redirect(url_for('welcome'))
                else:
                    flash('Invalid username or password. Please try again 🤪')
            else:
                flash('User does not exist. Please sign up 🙂')
    # Redirect to login page in case of GET request
    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        # Connect to DB and create a cursor
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()
             # Check if username exists in DB, If NO then add in DB and redirect to welcome page
             # Otherwise username already exists.
            if user:
                #flash('Username already exists. Please choose a different one 🧐')
                return jsonify(success=False, error="Username already exists."), 400
            else:
                #cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                cur.execute("INSERT INTO users (username, password, first_name, last_name, email, security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, first_name, last_name, email, security_question, security_answer))
                conn.commit()
                session['username'] = username
                return redirect(url_for('welcome'))
    # Redirect to login page in case of GET request
    #return redirect(url_for('login'))
    return render_template('signup.html')


# Default method is GET in flask if nothing is mentioned
# If POST method is mentioned in route, then the route will only accept POST requests


# Route for welcome page, if user directly want to access the welcome page
# Then check if user's login session is still active, otherwise send to login page
@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Route to log user put of session
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
    

# @app.route('/booking')
# def booking():
#     if 'username' in session:
#         return render_template('booking.html', username=session['username'])
#     else:
#         return redirect(url_for('login'))

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            # Extract form data
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            trip = request.form['trip']
            date = request.form['date']
            # Insert data into the database
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                # Insert data into bookings table
                cur.execute("INSERT INTO bookings (username, name, email, phone, trip, date) VALUES (?, ?, ?, ?, ?, ?)", (username, name, email, phone, trip, date))
                # Commit the transaction
                conn.commit()
                # Flash a success message
                #flash("Congratulations 🎉, " + name + "! Your trip to " + trip + " on " + date + " has been booked. 🥳")
            # Redirect to the booking page         
            #return redirect(url_for('booking'))
            # Return a JSON response on calling the API, instead of redirecting
            return jsonify({'status': 'success', 'message': f'Congratulations 🎉, {name}! Your trip to {trip} on {date} has been booked. 🥳'})
        # GET request
        else:
            return render_template('booking.html', username=username)
    return redirect(url_for('login'))


@app.route('/manage_booking')
def manage_booking():
    if 'username' in session:
        #get the username of the logged-in user
        username = session['username']
        with sqlite3.connect('database.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
             # fetch the bookings of the logged-in user
            cur.execute("SELECT * FROM bookings WHERE username=?", (username,))
            # Fetch all rows as a list of dictionaries for easy use in the template
            bookings = [dict(row) for row in cur.fetchall()]
            # Pass the booking data to the booking_details.html template
            return render_template('manage_bookings.html', username=username, bookings=bookings)
    else:
        return redirect(url_for('login'))


@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    booking_id = request.form.get('booking_id')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
        conn.commit()
    #return redirect(url_for('manage_booking'))
    return jsonify({'status': 'success', 'message': 'Booking canceled successfully'})


# can you create a route for resetting the password
@app.route('/reset_password', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        new_password = request.form['new_password']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND email=? AND security_question=? AND security_answer=?", (username, email, security_question, security_answer))
            user = cur.fetchone()
            if user:
                cur.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
                conn.commit()
                return jsonify(success=True), 200
            else:
                return jsonify(success=False, error="Invalid credentials"), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)