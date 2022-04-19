from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    name = StringField('Full name', [validators.Length(min=1, max=64)])
    username = StringField('Username', [validators.Length(min=4, max=64)])
    email = StringField('Email', [validators.Length(min=6, max=64)])
    password = PasswordField('Password', [validators.input_required()])


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=64)])
    password = PasswordField('Password', [validators.input_required()])


class TransactionForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=64)])
    amount = StringField('Amount', [validators.Length(min=1, max=50)])


class BuyForm(FlaskForm):
    amount = StringField('Amount', [validators.Length(min=1, max=50)])
