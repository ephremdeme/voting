from flask_login import UserMixin
from flask_principal import RoleNeed, UserNeed
from flask_sqlalchemy import BaseQuery
from werkzeug.utils import cached_property
from . import create_app
from . import db
import jwt
import datetime


class UserQuery(BaseQuery):

    def from_identity(self, identity):
        """
        Loads user from flask.ext.principal.Identity instance and
        assigns permissions from user.
        A "user" instance is monkeypatched to the identity instance.
        If no user found then None is returned.
        """

        try:
            user = self.get(int(identity.name))
        except ValueError:
            user = None

        if user:
            print("userrrrrr")
            identity.provides.update(user.provides)

        identity.user = user

        return user


class User(UserMixin, db.Model):
    MEMBER = "member"
    ADMIN = "admin"

    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    votes = db.relationship('Vote', backref='author', lazy=True)

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'), UserNeed(self.id)]
        if self.is_member:
            needs.append(RoleNeed('member'))
        if self.is_admin:
            needs.append(RoleNeed('admin'))
        return needs

    @property
    def is_member(self):
        return self.role == self.MEMBER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                create_app().config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, create_app().config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Vote(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    vote_name = db.Column(db.String(100), default='')
    hash = db.Column(db.String(100), default='', unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Vote('{self.vote_name}', '{self.hash}')"

    def toJson(self):
        return {
            "id": self.id,
            "vote_name": self.vote_name,
            "hash": self.hash,
        }
