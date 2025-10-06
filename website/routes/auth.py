import json, os, pathlib
import requests
import hashlib
from urllib.parse import urlencode

from flask import *
from flask_login import *
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
    if len(doc)==0: return {"msg": "Wrong email or password"}, 401
    doc = doc[0]
    data = doc.to_dict()
    pwhash = data["password"]
    if not check_password_hash(pwhash, password): return {"msg": "Wrong email or password"}, 401

    if not User.query.get(doc.id):
        new_user = User(id=doc.id, username=data["username"])
        db.session.add(new_user)
        db.session.commit()
    
    # access_token = create_access_token(identity=doc.id)
    # refresh_token = create_refresh_token(identity=doc.id)

    login_user(User.query.get(doc.id))
    
    return {
        "msg": "success",
        # "access_token": access_token,
        # "refresh_token": refresh_token,
    }

@login_required
def logout():
    logout_user()
    return {"msg": "success"}

@bp.route("/profile")
@login_required
def profile():
    user:User = current_user
    if not user.is_active:
        return {"msg": "User not found"}, 404
    
    return {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "nickname": user.nickname,
        "rating": user.rating,
    }
