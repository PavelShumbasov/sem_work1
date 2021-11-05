from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .menu import menu
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me") == ""
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='alert alert-success')
                login_user(user, remember=remember_me)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='alert alert-danger')
        else:
            flash('Email does not exist.', category='alert alert-danger')

    return render_template("login.html", user=current_user, menu=menu)


@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get("email")
        username = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='alert alert-danger')
        elif username_exists:
            flash('Username is already in use.', category='alert alert-danger')
        elif password1 != password2:
            flash('Password do not match!', category='alert alert-danger')
        elif len(username) < 5:
            flash('Username is too short.', category='alert alert-danger')
        elif len(password1) < 6:
            flash('Password is too short.', category='alert alert-danger')
        elif len(email) < 4:
            flash("Email is invalid.", category='alert alert-danger')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='alert alert-success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user, menu=menu)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out!", category="alert alert-info")
    return redirect(url_for("views.home"))


@auth.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists and email_exists.email != current_user.email:
            flash('Email is already in use.', category='alert alert-danger')
        elif username_exists and username_exists.username != current_user.username:
            flash('Username is already in use.', category='alert alert-danger')
        elif password1 != password2:
            flash('Password do not match!', category='alert alert-danger')
        elif len(username) < 5:
            flash('Username is too short.', category='alert alert-danger')
        elif len(password1) < 6:
            flash('Password is too short.', category='alert alert-danger')
        elif len(email) < 4:
            flash("Email is invalid.", category='alert alert-danger')
        else:
            current_user.email = email
            current_user.username = username
            current_user.password = generate_password_hash(password1, method='sha256')
            db.session.commit()
            login_user(current_user, remember=True)
            flash('User updated!', category="alert alert-info")
            return redirect(url_for('views.home'))

    return render_template("edit_profile.html", user=current_user, menu=menu)
