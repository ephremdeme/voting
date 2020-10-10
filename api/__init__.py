from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, identity_loaded
from flask_cors import CORS


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.run(host='0.0.0.0')
    app.config['SECRET_KEY'] = '9OLWxNauth_blueprintD4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    principals = Principal(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(user_id)

    @principals.identity_loader
    def read_identity_from_flask_login():
        if current_user.is_authenticated:
            return Identity(current_user.id)
        return AnonymousIdentity()

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if not isinstance(identity, AnonymousIdentity):
            identity.provides.update(current_user.provides)

    from .BlockchainAPINode import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
