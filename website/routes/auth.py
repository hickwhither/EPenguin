import json, os, pathlib
import requests
import hashlib
from urllib.parse import urlencode

from flask import *
from flask_login import *
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    unset_jwt_cookies,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    current_user,
)

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
    
    access_token = create_access_token(identity=doc.id)
    refresh_token = create_refresh_token(identity=doc.id)

    login_user(User.query.get(doc.id))
    
    return {
        "msg": "success",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "success"})
    unset_jwt_cookies(response)
    return response

@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}

@bp.route("/profile")
@jwt_required()
def profile():
    # print(current_user)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404
    
    return {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "nickname": user.nickname,
        "rating": user.rating,
    }
