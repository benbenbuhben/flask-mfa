import re
import random

from flask import render_template, flash, redirect, url_for, session, request
from app import app, db, twilio_client, twilio_phone, twilio_service_sid, logger
from datetime import datetime, timedelta

from .forms import LoginForm, RegisterForm, AuthenticationForm, VerificationForm
from app.models import User, TemporaryCode


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    email = session.get('email')
    return render_template('home.html', email=email)


#-----------------------REGISTER-------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()  # Create an instance of the registration form
    if form.validate_on_submit():  # Validate the form
        email = form.email.data
        password = form.password.data
        phone = form.phone.data

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))  # Redirect back to the registration page


        # Save user to the database
        new_user = User(email=email,phone=phone)
        new_user.set_password(password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template("register.html", form=form)  # Pass the form to the template
#----------------------- LOGIN AND MFA-------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    isValid = form.validate_on_submit()
    print("Login is valid", isValid)
    if isValid:
        email = form.email.data  
        password = form.password.data  

        # Check the email and password against your database
        user = User.query.filter_by(email=email).first()  # Fetch user from the database

        if user is None:
            flash('No account found with that email. Please check and try again.', 'danger')
            return redirect(url_for('login'))
        if user and user.check_password(password): 
            mfa_code = f"{random.randint(100_000, 999_999)}"
            print(user.email, mfa_code)
            expires_at = datetime.utcnow() + timedelta(minutes=5)
            temp_code = TemporaryCode(user_id=user.id, phone=user.phone,
                                      code=mfa_code, expires_at=expires_at)
            
            db.session.add(temp_code)
            db.session.commit()

            print(twilio_phone, user.phone)
            # Send the message to phone
            message = twilio_client.messages.create(
                body=f"Your MFA code is: {mfa_code}",
                from_=twilio_phone,
                to=user.phone
            )
            print(message.body)

            session['user_id'] = user.id 
            flash('A verification code has been sent to your phone.', 'info')
            return redirect(url_for('mfa')) 
        else:
            flash('Invalid email or password.', 'danger') 
    print("Just rendering template")
    return render_template('login.html', form=form)  


@app.route("/mfa", methods=["GET", "POST"])
def mfa():
    form = AuthenticationForm()
    
    if form.validate_on_submit():
        pin = form.pin.data  # Get the pin from the form
        user_id = session.get('user_id')  # Get the user_id from the session

        if not user_id:
            flash('Session expired. Please log in again.', 'danger')
            return redirect(url_for('login'))

        # Fetch the most recent temporary code for this user
        temp_code = TemporaryCode.query.filter_by(user_id=user_id).order_by(TemporaryCode.created_at.desc()).first()

        # Check if the pin matches and is not expired
        if temp_code and temp_code.code == pin and temp_code.expires_at > datetime.utcnow():
            flash('MFA successful!', 'success')
            session['authenticated'] = True  # Mark the user as authenticated
            return redirect(url_for('dashboard'))  # Redirect to the dashboard or another protected page
        else:
            flash('Invalid or expired code. Please try again.', 'danger')

    return render_template('mfa.html', form=form)