from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_login import LoginManager


import os, importlib

import firebase_admin
cred = firebase_admin.credentials.Certificate("cktoj-users-abcxyzhehe-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

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
    socketio.init_app(app)

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-CSRFToken"],
    )

    scheduler.init_app(app)
    scheduler.start()

    # Loading bp
    blueprints = ['api', 'auth', 'updater']
    for i in blueprints:
        bp = importlib.import_module(f'website.routes.{i}', 'bp').bp
        app.register_blueprint(bp)

    from .models import User
    login_manager = LoginManager()
    # login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


    create_database(app)
    return app

