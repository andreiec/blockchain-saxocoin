from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from passwords import _mysql_password
from sqlhelpers import *
from forms import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = _mysql_password
app.config['MYSQL_DB'] = 'saxocoin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'secret123'

mysql = MySQL(app)


def log_in_user(username):
    users = Table('user', 'name', 'email', 'username', 'password')
    user = users.getone('username', username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')


@app.route("/")
def index():
    send_coin('andreiec', 'mihai', 200)
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", session=session)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.form)

        if form.validate():
            username = form.username.data
            password = form.password.data

            users = Table('user', 'name', 'username', 'email', 'password')
            user = users.getone('username', username)

            # user[4] is the password
            try:
                accpass = user.get('password')
            except:
                return render_template('login.html', form=form)

            if accpass == password:
                log_in_user(username)

                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    users = Table('user', 'name', 'username', 'email', 'password')

    if request.method == "POST":
        form = RegisterForm(request.form)

        if form.validate():
            name = form.name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data

            users.insert(name, username, email, password)

            log_in_user(username)

            return redirect(url_for('dashboard'))

    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
