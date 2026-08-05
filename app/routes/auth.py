from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required

from flask_login import login_user, logout_user, current_user

from app.extensions import db, bcrypt

from app.models.user import User

auth = Blueprint("auth", __name__)

from flask_login import current_user

@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")

        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")

    


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Password Match Check
        if password != confirm_password:

            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.signup"))

        # Duplicate Email Check
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            flash("Email already exists.", "danger")
            return redirect(url_for("auth.signup"))

        # Hash Password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(

            full_name=full_name,
            email=email,
            password=hashed_password

        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("main.home"))