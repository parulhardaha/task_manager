from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User
from forms import SignupForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


# Import app and login_manager after other imports to avoid circular import
from main import app, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already exists")
            return redirect(url_for("signup"))

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role=form.role.data
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid credentials")

    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))