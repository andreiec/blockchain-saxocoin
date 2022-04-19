from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from passwords import _mysql_password
from sqlhelpers import *
from forms import *
import time


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
    blockchain = get_blockchain().chain
    return render_template("index.html", blockchain=blockchain)


@app.route("/dashboard")
def dashboard():
    blockchain = get_blockchain().chain
    ct = time.strftime("%I:%M %p")
    balance = get_balance(session.get('username'))

    return render_template("dashboard.html", session=session, ct=ct, balance=balance, blockchain=blockchain, page='dashboard')


@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    form = TransactionForm()
    balance = get_balance(session.get('username'))

    if request.method == "POST":
        form = TransactionForm(request.form)

        try:
            send_coin(session.get('username'), form.username.data, form.amount.data)
            return redirect(url_for('dashboard'))
        except Exception as e:
            return redirect(url_for('transaction'))

    return render_template('transaction.html', session=session, balance=balance, form=form, page='transaction')


@app.route("/buy", methods=['GET', 'POST'])
def buy():
    form = BuyForm()
    balance = get_balance(session.get('username'))

    if request.method == "POST":
        form = BuyForm(request.form)

        try:
            send_coin('admin', session.get('username'), form.amount.data)
            return redirect(url_for('dashboard'))
        except Exception as e:
            return redirect(url_for('buy'))

    return render_template('buy.html', session=session, balance=balance, form=form, page='buy')


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
