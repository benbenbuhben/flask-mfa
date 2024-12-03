from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField(
        'Phone', 
        validators=[
            DataRequired(),
            Regexp(r'^\+[0-9]{11,12}$', message="Phone number must be in the format +[country code][number], e.g., +12065550103.")
        ]
    )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AuthenticationForm(FlaskForm):
    mfa_code = PasswordField('Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Verify")

class VerificationForm(FlaskForm):
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify')

class ChangePhoneForm(FlaskForm):
    phone = StringField(
        'New Phone Number', 
        validators=[
            DataRequired(),
            Regexp(r'^\+[0-9]{11,12}$', message="Phone number must be in the format +[country code][number], e.g., +12065550103.")
        ]
    )
    submit = SubmitField("Update Phone Number")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password', 
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        'New Password', 
        validators=[
            DataRequired(), 
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password', 
        validators=[
            DataRequired(), 
            EqualTo('new_password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Update Password')
