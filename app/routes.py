import secrets
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    Blueprint)
from datetime import datetime
from . import db, twilio_client, twilio_phone, twilio_content_sid
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangePhoneForm, AuthenticationForm
from .models import User, TemporaryCode


main_bp = Blueprint('main', __name__)
LOGIN_URL = "main.login"
CHANGE_PASS_TEMPLATE = 'change_password.html'
@main_bp.route('/')
def index():
    return redirect(url_for(LOGIN_URL))

@main_bp.route('/home')
def home():
    if session.get("user_id") is not None and session.get("authenticated"):
        user_id = session.get('id')
        return render_template('home.html', id=user_id)
    else:
        return redirect(url_for(LOGIN_URL))

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()  # Create an instance of the registration form
    if form.validate_on_submit():  # Validate the form
        email = form.email.data
        password = form.password.data
        phone = form.phone.data

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('main.register'))  # Redirect back to the registration page

        new_user = User(email=email, phone=phone)
        new_user.set_password(password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for(LOGIN_URL))  # Redirect to login page after successful registration

    return render_template("register.html", form=form)

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)  
    if form.validate_on_submit():
        email = form.email.data  
        password = form.password.data  

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('No account found with that email. Please check and try again.', 'danger')
            return redirect(url_for(LOGIN_URL))
        if not user.check_password(password):
            flash('Wrong password. Please check and try again.', 'danger')
            return redirect(url_for(LOGIN_URL))
        if user.valid_lastlogin():
            session["user_id"] = user.id
            session["authenticated"] = True
            user.update_lastlogin()
            db.session.commit()
            flash("Welcome back!", "success")
            return redirect(url_for("main.home"))

        
        mfa_code = f"{secrets.randbelow(10**6):06d}"
        temp_code = TemporaryCode(
            user_id=user.id, 
            phone=user.phone, 
            code=mfa_code
        )
        db.session.add(temp_code)
        db.session.commit()

        twilio_client.messages.create(
            from_=twilio_phone,
            content_sid=twilio_content_sid,
            content_variables='{"1":"' + mfa_code + '"}',
            to=f"whatsapp:{user.phone}"
        )

        session['user_id'] = user.id
        session['from_login'] = True
        flash('A verification code has been sent to your phone.', 'info')
        return redirect(url_for('main.mfa')) 
    return render_template('login.html', form=form)

@main_bp.route('/mfa', methods=['GET', 'POST'])
def mfa():
    # if not session.pop('from_login', False):
    #     flash('Unauthorized access to MFA. Please log in.', 'danger')
    #     return redirect(url_for(LOGIN_URL))
    form = AuthenticationForm()
    if form.validate_on_submit():
        pin = form.mfa_code.data  
        user_id = session.get('user_id')  

        if not user_id:
            flash('Session expired. Please log in again.', 'danger')
            return redirect(url_for(LOGIN_URL))

        temp_code = TemporaryCode.query.filter_by(user_id=user_id).order_by(TemporaryCode.created_at.desc()).first()

        if temp_code and temp_code.code == pin and temp_code.expires_at > datetime.now():
            session['authenticated'] = True
            user = User.query.get(user_id)  # Adjust based on how the user is retrieved
            user.update_lastlogin()
            db.session.commit()
            return redirect(url_for('main.home'))  

        else:
            flash('Invalid or expired code. Please try again.', 'danger')

    return render_template('mfa.html', form=form)

@main_bp.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('user_id', None) 
    session.pop('authenticated', None)  
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for(LOGIN_URL))

@main_bp.route("/change_phone", methods=["GET", "POST"])
def change_phone():
    form = ChangePhoneForm()
    user_id = session.get('user_id')
    authenticated = session.get("authenticated")
    if form.validate_on_submit() and user_id and authenticated:
        phone = form.phone.data
        user = db.session.get(User, user_id)
        if user:
            user.phone = phone
            db.session.commit()
            flash('Phone number updated successfully.', 'success')
        else:
            flash("User not found.", "danger")
        return redirect(url_for("main.home"))
    elif user_id is None or authenticated is None:
        flash("Please log in first.", "danger")
        return redirect(url_for(LOGIN_URL))
    return render_template("change_phone.html", form=form)

@main_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    user_id = session.get("user_id")
    if form.validate_on_submit() and user_id:
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        user = db.session.get(User, user_id)
        if not user:
            flash("User is not found", "danget")
            return redirect(url_for(LOGIN_URL))
        if user.check_password(current_password):  # Check current password
            if new_password == confirm_password:  # Check if new passwords match
                user.set_password(new_password)  # Set the new password
                db.session.commit()
                flash('Password updated successfully!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('New passwords do not match.', 'danger')
                return render_template(CHANGE_PASS_TEMPLATE, form=form)

        else:
            flash('Current password is incorrect.', 'danger')
            return render_template(CHANGE_PASS_TEMPLATE, form=form)
    return render_template(CHANGE_PASS_TEMPLATE, form=form)


@main_bp.route("/debug_login", methods=["GET"])
def debug_login():
    form = LoginForm()
    rendered_template = render_template("login.html", form=form)
    print(rendered_template)  # Print to console for debugging
    return rendered_template