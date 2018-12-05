import re
from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnection
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "make it so number one"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def root():
    return render_template('registration.html')

@app.route('/welcome', methods=['POST'])
def hello():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    pwtest = request.form['password']
    swtest = request.form['conpassword']
    teststr = request.form['firstname']
    lastname = request.form['lastname']
    if not teststr.isalpha() or not lastname.isalpha():
        flash("Names must be all alphanumeric characters.")
    elif len(teststr) < 2 or len(lastname) < 2:
        flash("Names must longer than two characters.")
    elif request.form['password']!=request.form['conpassword']:
        flash("Password must match.")
    elif len(swtest) < 8 or len(pwtest) < 8:
        flash("Password must be at least eight characters")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address.")
    
    else:
        flash("Registration successfully completed")
        query = "INSERT INTO users (fname, lname, email, hpwd) VALUES (%(f)s, %(l)s, %(e)s, %(h)s);"
        data = {
            'f': request.form['firstname'],
            'l': request.form['lastname'],
            'e': request.form['email'],
            'h': pw_hash
            }
        db = MySQLConnection('login')
        insert = db.query_db(query, data)
        print(data)
        return render_template('welcome.html')
    return render_template('registration.html')

@app.route('/login', methods=["POST"])
def login():
    flash('Hello')
    mysql = MySQLConnection("login")
    query = "SELECT * FROM users WHERE email = %(e)s;"
    data = { "e" : request.form["email"]}
    result = mysql.query_db(query, data)
    if result:
        if bcrypt.check_password_hash(result[0]['hpwd'], request.form['password']):
            session['userid'] = result[0]['id']
            return render_template('welcome.html')
    flash("Please check password")
    test = bcrypt.generate_password_hash(request.form['password'])
    #if not EMAIL_REGEX.match(request.form['email']):
    #    flash("Invalid email address!")
    #    return render_template('registration.html')
    return render_template('registration.html')

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('registration.html')

if __name__=='__main__':
    app.run(debug=True)
