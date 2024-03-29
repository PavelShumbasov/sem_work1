from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()
SQLITE_DB = 'sqlite:///{}'.format(path.join(path.dirname(__file__), 'database.db'))


def create_app(params=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "qwe123asd"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if params:
        app.config['TESTING'] = params['TESTING']
        app.config["DATABASE"] = params['DATABASE']
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_DB
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from web_site.models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("web_site/" + 'database.db'):
        db.create_all(app=app)
