from flask import Blueprint, request, make_response, jsonify
from src.models.models import User, Group, BlacklistToken, session_db
from datetime import datetime

auth_blueprint = Blueprint("authAPI", __name__, url_prefix="/api/auth")


def validate_auth_form(form: dict) -> str:
    username = form.get("username")
    password = form.get("password")

    if not username:
        return "Username is required."

    if not password:
        return "Password is required."

    return ""


@auth_blueprint.route("/register", methods=["POST"])
def register():
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    username = post_data.get("username")
    password = post_data.get("password")
    groups = post_data.get("groups")

    if groups is None:
        response = {
            "status": "fail",
            "message": "Groups are required. Submit at least empty list",
        }
        return make_response(jsonify(response)), 400

    with session_db() as s:
        exist_user = (
            s.query(User)
            .filter(User.name == username, User.password == password)
            .first()
        )
        if exist_user:
            response = {
                "status": "fail",
                "message": "User already exists. Please Log In",
            }
            return make_response(jsonify(response)), 400
        else:
            new_user = User(name=username, password=password)
            s.add(new_user)
            for group in groups:
                existing_group = s.query(Group).filter(Group.id == group).first()
                new_user.groups.append(existing_group)
            s.commit()
            resp = {
                "status": "success",
                "message": "Successfully registered. Please Login",
            }
            return make_response(jsonify(resp)), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    post_data = request.get_json()

    username = post_data.get("username")
    password = post_data.get("password")

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    with session_db() as s:
        exist_user = (
            s.query(User)
            .filter(User.name == username, User.password == password)
            .first()
        )

        if not exist_user:
            responseObject = {
                "status": "fail",
                "message": "User/Password incorrect. Please try again.",
            }
            return make_response(jsonify(responseObject)), 400

        auth_token = exist_user.endcode_auth_token()
        responseObject = {
            "status": "success",
            "message": "Successfully logged in.",
            "auth_token": auth_token,
        }

        return make_response(jsonify(responseObject)), 200


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if not token:
        responseObject = {"status": "fail", "message": "Missing Authorization Header"}
        return make_response(jsonify(responseObject)), 400

    user_id, err = User.decode_auth_token(auth_token=token)

    if err:
        responseObject = {"status": "fail", "message": err}
        return make_response(jsonify(responseObject)), 400

    with session_db() as s:
        blacklisted = BlacklistToken(token=token, blacklisted_on=datetime.now())
        s.add(blacklisted)
        s.commit()

    responseObject = {"status": "success", "message": "Successfully logged out."}
    return make_response(jsonify(responseObject)), 200


@auth_blueprint.route("/delete", methods=["POST"])
def delete():
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    username = post_data.get("username")
    password = post_data.get("password")

    with session_db() as s:
        user = (
            s.query(User)
            .filter(User.name == username, User.password == password)
            .first()
        )
        user.groups.clear()
        user.favorites.clear()
        s.query(User).filter(User.name == username, User.password == password).delete()
        s.commit()

    responseObject = {"status": "success", "message": "Successfully deleted user."}
    return make_response(jsonify(responseObject)), 200
