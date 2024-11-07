import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])  # Assuming format 2065550103
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AuthenticationForm(FlaskForm):
    pin = PasswordField('Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Verify")

class VerificationForm(FlaskForm):
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify')