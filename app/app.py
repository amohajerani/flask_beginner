"""
Python Flask WebApp Auth0 integration example
"""

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import os
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, request, Response
from s3_functions import upload_file, get_file_names, get_file_obj, s3_delete_file
from mongo import get_username, insert_file_doc, file_exists, get_file_doc, mongo_delete_doc, mongo_update_file
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
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    wrapper.__name__ = func.__name__
    return wrapper
# Controllers API


@app.route("/")
def home():
    if not session.get('user'):
        return render_template('landing.html')
    username = get_username(session['user']['userinfo']['email'])
    contents = get_file_names(BUCKET, username)
    doc_objects = {}
    for content in contents:
        doc_objects[content] = get_file_doc(username+'/'+content)['private']
    print('doc object: ', doc_objects)
    return render_template('home.html', doc_objects=doc_objects, username=username)


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri='https://www.thegagali.com/callback'
    )


@app.route("/logout")
@require_auth
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
@require_auth
def upload():
    if request.method == "POST":
        f = request.files['file']
        private = len(request.form.getlist('private'))
        filename = secure_filename(f.filename)
        username = get_username(session['user']['userinfo']['email'])

        # check if a file with this name exists
        if file_exists(username, filename):
            return "file name exists. Pick a different name"
        # otherwise create a file doc
        insert_file_doc(username, filename, private)
        # Upload the file
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        upload_file(os.path.join(UPLOAD_FOLDER, filename),
                    BUCKET, username, filename)
        os.remove(os.path.join(UPLOAD_FOLDER, filename))

        return redirect("/")


@app.route("/<username>/<filename>")
def get_file(username, filename):
    filepath = username+'/'+filename

    # get the private attribute of the object
    file_doc = get_file_doc(filepath)

    if file_doc['private']:
        if not session.get('user'):
            return "Private file"
        session_username = get_username(session['user']['userinfo']['email'])
        if username != session_username:
            return "Private file"

    file_obj = get_file_obj(filepath, BUCKET)

    return Response(
        file_obj['Body'].read(), content_type=file_obj['ResponseMetadata']['HTTPHeaders']['content-type']
    )


@app.route("/delete/<username>/<filename>")
@require_auth
def delete_file(username, filename):
    filepath = username+'/'+filename
    # delete file doc from mongo db
    mongo_delete_doc(filepath)
    # delete from s3
    s3_delete_file(filepath, BUCKET)
    return redirect('/')


@app.route("/update-page/<username>/<filename>")
# @require_auth
def update_page(username, filename):
    filepath = username+'/'+filename
    file_doc = get_file_doc(filepath)
    private = file_doc['private']
    return render_template('update-page.html', filename=filename, username=username, private=private)


@app.route("/update-func/<username>/<filename>", methods=['POST'])
# @require_auth
def update_func(username, filename):
    if request.method == "POST":
        private = len(request.form.getlist('private'))
        filepath = username+'/'+filename
        mongo_update_file(filepath, {'private': private})
        return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 8000))
