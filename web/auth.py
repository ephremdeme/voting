from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask_principal import Permission, RoleNeed
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

admin_permission = Permission(RoleNeed('admin'))


@auth.route('/login', methods=["GET"])
def login():
    return render_template('login.html')


@auth.route('/admin')
@admin_permission.require(401)
def do_admin_index():
    return Response('Only if you are an admin')


@auth.route('/login', methods=["POST"])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    print(user)
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user:
        flash('Please check your email address details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page
    if not check_password_hash(user.password, password):
        flash('Please check your password details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=["GET"])
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    print(email)

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, role="admin", password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(
        email=email).first()
    login_user(user)
    # add the new user to the database

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
