from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app,'emails')
app.secret_key = "hehehehehe"


@app.route('/')
def index():
    if session.get('error_message', None) == None:
        session['error_message'] = ""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def add():
    input_email = request.form['email']
    #check that email is valid
    #if email is invalid, redirect to index
    if not EMAIL_REGEX.match(input_email):
        session['error_message'] = "Email is not valid!"
        return redirect('/', )
    #if email is valid, carry on
    else:
        session['error_message'] = ""
        query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
        data = {'email' : input_email}
        session['email'] = input_email
        mysql.query_db(query, data)
        return redirect('/success')


@app.route('/success')
def success():
    emails = mysql.query_db("SELECT id, email, DATE_FORMAT(created_at, '%b %D, %Y') AS created_at FROM emails")
    return render_template('success.html', emails=emails)

@app.route('/delete/<user_id>')
def delete(user_id):
    query = "DELETE FROM emails WHERE id = :id"
    data = {"id": user_id}
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)