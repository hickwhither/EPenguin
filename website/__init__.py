from flask import Flask,render_template
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

from werkzeug.security import generate_password_hash

import os, importlib

db = SQLAlchemy()
DB_NAME  = 'database.db'

socketio = SocketIO()
scheduler = APScheduler()

def create_database(app):
    with app.app_context():
        db.create_all()
    print("Database created")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    # CORS(app, origins=["*"])
    scheduler.init_app(app)
    scheduler.start()

    # Loading bp
    blueprints = ['api', 'auth', 'updater']
    for i in blueprints:
        bp = importlib.import_module(f'website.routes.{i}', 'bp').bp
        app.register_blueprint(bp)

    from .models import User

    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    socketio.init_app(app)

    return app

