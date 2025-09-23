import json, os, pathlib
import requests
import hashlib
from urllib.parse import urlencode

from flask import *
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from werkzeug.security import check_password_hash

from firebase_admin import firestore
firestore_client = firestore.client()
users_ref = firestore_client.collection("user")
from google.cloud.firestore import FieldFilter

from website import db
from website.models import User

bp = Blueprint('auth', __name__, url_prefix='/')

from datetime import datetime, timezone, timedelta

@bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(days=2))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError): # no valid jwt
        return response

@bp.route("/token", methods=["POST"])
def token():
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

    return {"access_token": create_access_token(identity=doc.id)}

@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@bp.route("/profile")
@jwt_required()
def profile():
    uid = get_jwt_identity()
    user:User = User.query.get(uid)
    return {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "name": user.name,
        "rating": user.rating,
    }
