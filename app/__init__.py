from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import os


db = SQLAlchemy()
DB_NAME = 'photo_blog.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("NEW_DB_URL", "sqlite:///blog.db") # second argument fallback, if DB specified in environment variable is not available, for example on local machine.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .auth import auth
    from .views import views
    

    Bootstrap(app)
    app.register_blueprint(auth)
    app.register_blueprint(views)

    from .models import User,PhotoPost,Comment
    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#def create_database(app):
#    if not path.exists(f'app/{DB_NAME}'):
#       db.create_all(app=app)
#       print('created database!')
