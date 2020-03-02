from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_mysqldb import MySQL
import MySQLdb.cursors
from prediction import user_ip
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
#app.config['PORT']='3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(app)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///'+'subbu.db'
# Enter your database connection details below
f = [11, 1, 1, 122, 12, 1, 12, 122, 2, 44, 2]
user_ip(f)
# Intialize MySQL
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        c = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        c.execute('SELECT * from accounts WHERE username=%s AND password=%s',(username, password))
        # Fetch one record and return result
        account = c.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template("index.html",msg=msg)
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        c = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        c.execute('SELECT * FROM accounts WHERE username = %s' , (username))
        account = c.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            c.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
@app.route('/pythonlogin/profile',methods=['GET', 'POST'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page

        c = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        c.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = c.fetchone()
        # Show the profile page with account info
        return render_template('prediction.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/profile/result', methods=['GET', 'POST'])
def result():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        if (request.method == 'POST'):
        # Create variables for easy access
            features = [int(request.form['age']), int(request.form['sex']), int(request.form['cp']),
                         int(request.form['trestbps']), int(request.form['restecg']),
                         int(request.form['talach']), int(request.form['exang']),
                         round(float(request.form['oldpeak']),1), int(request.form['slope']),
                         int(request.form['ca']), int(request.form['thal'])]
            print(features)
            #f = [11, 1, 1, 122, 12, 1, 12, 122, 2, 44, 2]
            if(user_ip(features)==1):
                return render_template('result1.html')
            else:
                return render_template('result.html')
        else:
            return render_template('prediction.html',msg='Please Fill All Details Correctly \n Note: All are numeric data')

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.debug=True
    app.run()