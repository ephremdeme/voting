import json

import jsonpickle
from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask.json import jsonify
from flask_principal import Permission, RoleNeed
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Vote
from . import db, token_required

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

admin_permission = Permission(RoleNeed('admin'))


@auth.route('/gui/login', methods=['POST'])
def gui_login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(email, password)
    user = User.query.filter_by(email=email).first()
    vote_array = []

    if user:
        for vote in user.votes:
            vote_array.append((vote.vote_name, vote.hash))

    return jsonify({'list': vote_array})


@auth.route('/login', methods=["POST"])
def login_post():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    print(user)
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user:
        flash('Please check your email address details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        # return redirect(url_for('auth.login'))

        return jsonify({
            "msg": "Please check your email address details and try again."
        })

    if not check_password_hash(user.password, password):
        flash('Please check your password details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        # return redirect(url_for('auth.login'))
        return jsonify({
            "msg": "Please check your password details and try again."
        })
    login_user(user)
    token = user.encode_auth_token(user.id)
    print(token)
    # if the above check passes, then we know the user has the right credentials
    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        },
        "token": token
    })


@auth.route('/signup', methods=['POST'])
def signup_post():

    data = request.get_json()
    email = data['email']
    name = data['name']
    password = data['password']

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    print(email)

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, role="admin",
                    password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(
        email=email).first()
    login_user(user)
    token = user.encode_auth_token(user.id)
    # add the new user to the database

    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        },
        "token": token
    })


@auth.route('/logout')
@token_required
def logout():
    logout_user()
    return {
        "message": "Successfully Logged Out"
    }


@auth.route('/get_user')
@token_required
def get_user(current_user):
    return jsonify({
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name
        }
    })
