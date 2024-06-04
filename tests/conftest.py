import pytest
from app import create_app
from src.db import db, migrate
from src.models.models import session_db
from flask import Flask

import requests

import tempfile
import os


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    # app = Flask(__name__)
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = "postgresql://postgres:password@localhost:5434/flask_db"

    # init_app(app)
    # db.init_app(app)
    # migrate.init_app(app, db)
    # app.run(port=8000)

    yield app


@pytest.fixture
def token():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "w", "password": "q"},
    )
    return resp.json()["auth_token"]


@pytest.fixture
def give_own_post_id(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    post_id = None
    for post in resp.json()["posts"]:
        if post["am_owner"] == True:
            post_id = post["id"]
            yield post_id


@pytest.fixture
def give_not_own_post_id(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    post_id = None
    for post in resp.json()["posts"]:
        if post["am_owner"] == False:
            post_id = post["id"]
            yield post_id
