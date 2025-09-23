import json, os, pathlib
import requests
import hashlib
from urllib.parse import urlencode

from flask import *
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash

from firebase_admin import firestore
firestore_client = firestore.client()
users_ref = firestore_client.collection("user")
from google.cloud.firestore import FieldFilter

from website import db
from website.models import User

bp = Blueprint('auth', __name__, url_prefix='/')

from datetime import datetime, timezone, timedelta

@bp.route("/signin", methods=["POST"])
def signin():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username==None or password==None: return {"msg": "Wrong email or password"}, 401
    
    doc = users_ref.where(filter=FieldFilter("username", "==", username)).get()
    if not doc: return {"msg": "Wrong email or password"}, 401
    doc = doc[0]
    data = doc.to_dict()
    pwhash = data["password"]
    if not check_password_hash(pwhash, password): return {"msg": "Wrong email or password"}, 401

    if not User.query.get(doc.id):
        new_user = User(id=doc.id, username=data["username"])
        db.session.add(new_user)
        db.session.commit()
    
    login_user(doc.id)
    return {"msg": "success"}

@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return {"msg": "success"}

@bp.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return {"id": 0}
    current_user:User
    return {
        "id": current_user.id,
        "username": current_user.username,
        "avatar": current_user.avatar,
        "name": current_user.name,
        "rating": current_user.rating,
    }
