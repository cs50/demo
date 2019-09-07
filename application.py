# https://manage.auth0.com/dashboard/us/cs50/applications/7DoKCwuk9LlkwUIY0ufkQ2dqMjaatuNI/quickstart

import os

from authlib.flask.client import OAuth
from flask import Flask, abort, redirect, render_template, session, url_for
from flask_session import Session
from werkzeug import security
from werkzeug.contrib.fixers import ProxyFix

# Application
app = Flask(__name__)

# ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

# Enable OAuth
oauth = OAuth(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Authlib
auth0 = oauth.register(
    "auth0",
    access_token_url="https://cs50.auth0.com/oauth/token",
    api_base_url="https://cs50.auth0.com",
    authorize_params={
        "connection": "harvard",  # Automatically select harvard
        "prompt": "login"  # Force login
    },
    authorize_url="https://cs50.auth0.com/authorize",
    client_id=os.environ.get("CLIENT_ID"),
    client_kwargs={
        "scope": "openid profile email"
    },
    client_secret=os.environ.get("CLIENT_SECRET")
)


# GET /
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# GET /login
@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=url_for("redirect_uri", _external=True))


# GET /logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# GET /redirect_uri
@app.route("/redirect_uri")
def redirect_uri():
    auth0.authorize_access_token()
    session["userinfo"] = auth0.get("userinfo").json()
    return redirect(url_for("index"))
