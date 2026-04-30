from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User
from forms import SignupForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return redirect(url_for("routes.login"))


@routes.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already exists")
            return redirect(url_for("routes.signup"))

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method="pbkdf2:sha256"),
            role=form.role.data
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("routes.login"))

    return render_template("signup.html", form=form)


@routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("routes.dashboard"))

        flash("Invalid credentials")

    return render_template("login.html", form=form)


@routes.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))

from models import Project

@routes.route("/projects")
@login_required
def projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)

from forms import ProjectForm
from models import Project
from flask_login import login_required, current_user

@routes.route("/create_project", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            created_by=current_user.id
        )

        db.session.add(project)
        db.session.commit()

        return redirect(url_for("routes.projects"))

    return render_template("create_project.html", form=form)