"""
Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import os
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request
from s3_functions import upload_file, list_files
from werkzeug.utils import secure_filename

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


UPLOAD_FOLDER = "uploads"
BUCKET = "thegagali"


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


def require_auth(func):
    def wrapper(*args, **kwargs):
        if session.get('user'):
            func(*args, **kwargs)
        else:
            return redirect('/login')
    wrapper.__name__ = func.__name__
    return wrapper
# Controllers API


@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/public")
def public():
    return render_template(
        "public.html")


@app.route("/private")
@require_auth
def private():
    return render_template(
        "private.html")


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri="https://www.thegagali.com/callback"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": "https://www.thegagali.com",
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/form")
@require_auth
def formfunc():
    return render_template('form.html')


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f.filename, BUCKET)
        os.remove(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))

        return redirect("/")


@app.route("/files")
def list():
    contents = list_files(BUCKET)
    return render_template('collection.html', contents=contents)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 8000))
