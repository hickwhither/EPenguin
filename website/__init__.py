from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os, importlib, datetime

import firebase_admin
cred = firebase_admin.credentials.Certificate("cktoj-users-abcxyzhehe-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

db = SQLAlchemy()
DB_NAME  = 'database.db'

jwt = JWTManager()
socketio = SocketIO()
scheduler = APScheduler()

def create_database(app):
    with app.app_context():
        db.create_all()
    print("Database created")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    
    app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=3)

    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    
    jwt.init_app(app)
    db.init_app(app)
    socketio.init_app(app)

    CORS(app, origins=["*"])
    scheduler.init_app(app)
    scheduler.start()

    # Loading bp
    blueprints = ['api', 'auth', 'updater']
    for i in blueprints:
        bp = importlib.import_module(f'website.routes.{i}', 'bp').bp
        app.register_blueprint(bp)

    from .models import User

    create_database(app)
    return app

