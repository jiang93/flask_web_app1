from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_name = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "i74FkLs9638u2xjA"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_name}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Note, User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/'+DB_name):
        with app.app_context():
            db.create_all()
            print('Created Database!')