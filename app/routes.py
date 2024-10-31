from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User
import re

from .forms import LoginForm, RegisterForm


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    email = session.get('email')
    return render_template('home.html', email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the form
    if form.validate_on_submit():
        email = form.email.data  # Get the email from the form
        password = form.password.data  # Get the password from the form

        # Check the email and password against your database
        user = User.query.filter_by(email=email).first()  # Fetch user from the database

        if user is None:
            flash('No account found with that email. Please check and try again.', 'danger')
            return redirect(url_for('login'))
        if user and user.check_password(password):  # Assuming you have a method to check passwords
            session['user_id'] = user.id  # Store user ID in the session
            session['email'] = user.email  # Store user ID in the session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to the home page after successful login
        else:
            flash('Invalid email or password.', 'danger')  # Flash an error message

    return render_template('login.html', form=form)  # Pass the form to the template



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

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save user to the database
        new_user = User(email=email, password=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template("register.html", form=form)  # Pass the form to the template