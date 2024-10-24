from flask import render_template, request
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        phone = request.form.get("phone", "")

        print(f"Username: {username}, Password: {password}, Phone: {phone}")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save user to the database
        new_user = User(username=username, password=hashed_password, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        return "Registration successful!"

    return render_template("register.html")
