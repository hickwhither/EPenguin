import json, os, pathlib
import requests
import hashlib
from urllib.parse import urlencode

from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests

google_client_secrets_file = "./google_client_secrets.json"
GOOGLE_CLIENT_ID = json.load(open("./google_client_secrets.json", "r")).get('web').get('client_id')

flow = Flow.from_client_secrets_file(
    client_secrets_file=google_client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=os.getenv('REDIRECT_URI')
)

from flask import *
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash

from website import db
from website.models import User

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route("/signin")
def signin():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@bp.route("/gCallback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if session.get("state") != request.args.get("state"):
        return redirect(url_for('auth.expired_state'))

    credentials = flow.credentials
    token_request = google.auth.transport.requests.Request()
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    email_encoded = id_info["email"].lower().encode('utf-8')
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    query_params = urlencode({'d': os.getenv('DEFAULT_AVATAR'), 's': '40'})
    avatar = f"https://www.gravatar.com/avatar/{email_hash}?{query_params}"

    user = User.query.filter_by(id=id_info["sub"]).first()
    if not user:
        user = User(
            id=id_info["sub"],
            email=id_info["email"],
            avatar=avatar,
            name=id_info["name"]
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect("/")

@bp.route('/expired_state')
def expired_state():
    return render_template("expired_state.html")


@bp.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect("/")
