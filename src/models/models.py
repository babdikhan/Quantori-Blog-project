from contextlib import contextmanager
import datetime
import jwt

from flask import current_app

from sqlalchemy.exc import SQLAlchemyError

from src.db import db


@contextmanager
def session_db():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise e


user_group = db.Table(
    "user_group",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id")),
)

user_favorite = db.Table(
    "user_favorite",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship("Posts", backref="user", lazy=True)
    groups = db.relationship("Group", secondary=user_group, backref="users", lazy=True)
    favorites = db.relationship(
        "Posts", secondary=user_favorite, backref="users", lazy=True
    )
    comments = db.Column(db.String(128))

    def endcode_auth_token(self):
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": self.id,
            }
            return jwt.encode(
                payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
            )
            return (payload["sub"], None)
        except jwt.ExpiredSignatureError:
            return (None, "Signature expired. Please log in again.")
        except jwt.InvalidTokenError:
            return (None, "Invalid token. Please log in again.")


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def serialize(self, user_id):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created": self.created,
            "am_owner": self.user_id == user_id,
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)
