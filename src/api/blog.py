from flask import Blueprint, request, make_response, jsonify
from src.models.models import User, Group, BlacklistToken, session_db, Posts, user_group

import functools

blog_blueprint = Blueprint("postAPI", __name__, url_prefix="/api/post")


def auth_required(handler):
    @functools.wraps(handler)
    def wrapped_view(**kwargs):
        token = request.headers.get("Authorization")
        if not token:
            responseObject = {
                "status": "fail",
                "message": "Missing Authorization Header",
            }
            return make_response(jsonify(responseObject)), 400

        with session_db() as s:
            query = (
                s.query(BlacklistToken).filter(BlacklistToken.token == token).first()
            )
            if query:
                responseObject = {
                    "status": "fail",
                    "message": "Token Blacklisted",
                }
                return make_response(jsonify(responseObject)), 400

        user_id, err = User.decode_auth_token(token)
        if err:
            responseObject = {"status": "fail", "message": err}
            return make_response(jsonify(responseObject)), 400

        return handler(**kwargs, user_id=user_id)

    return wrapped_view


def validate_post_form(form: dict) -> str:
    title = form.get("title")
    body = form.get("body")

    if not title:
        return "Title is required."

    if not body:
        return "Body is required."

    return ""


@blog_blueprint.route("/", methods=["GET"])
@auth_required
def index(user_id):
    with session_db() as s:
        # groups_where_user_is
        query = s.query(user_group).all()
        user_groups = []
        for group in query:
            if user_id == group[0]:
                user_groups.append(group[1])
        # users_with_the_same_group
        users = set([user_id])
        for group in query:
            if group[1] in user_groups:
                users.add(group[0])

        query = s.query(Posts)
        query = query.join(User, User.id == Posts.user_id)
        query = query.where(Posts.user_id.in_((users)))
        posts = query.all()
        responseObject = {
            "status": "success",
            "message": "Posts successfully retrieved",
            "posts": [post.serialize(user_id) for post in posts],
        }
        return make_response(jsonify(responseObject)), 200
    return (
        make_response(
            jsonify(
                {"status": "fail", "message": "Server is down, please try again later"}
            )
        ),
        500,
    )


@blog_blueprint.route("/create", methods=["POST"])
@auth_required
def create(user_id: int):
    post_data = request.get_json()
    if err := validate_post_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    title = post_data["title"]
    body = post_data["body"]

    with session_db() as s:
        new_post = Posts(title=title, body=body, user_id=user_id)
        s.add(new_post)
        s.commit()
        response = {"status": "success", "message": "Post successfully created"}
        return make_response(jsonify(response)), 400


@blog_blueprint.route("/update/<int:id>", methods=["POST"])
@auth_required
def update(id: int, user_id: int):
    post_data = request.get_json()

    if err := validate_post_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    title = post_data["title"]
    body = post_data["body"]

    with session_db() as s:
        post = s.query(Posts).get(id)
        if not post:
            response = {"status": "fail", "message": f"Failed to Find Post: {id}"}
            return make_response(jsonify(response)), 404

        if post.user_id != user_id:
            response = {"status": "fail", "message": "Can't edit someone else's post"}
            return make_response(jsonify(response)), 400

        post.body = body
        post.title = title
        s.commit()
        response = {"status": "success", "message": "Post updated"}
        return make_response(jsonify(response)), 200


@blog_blueprint.route("/delete/<int:id>", methods=["POST"])
@auth_required
def delete(id: int, user_id: int):
    with session_db() as s:
        post = s.query(Posts).get(id)
        if not post:
            response = {"status": "fail", "message": f"Failed to Find Post: {id}"}
            return make_response(jsonify(response)), 404

        if post.user_id != user_id:
            response = {"status": "fail", "message": "Can't delete someone else's post"}
            return make_response(jsonify(response)), 400

        post = s.query(Posts).filter(Posts.id == id).delete()
        s.commit()
        response = {"status": "success", "message": "Post deleted"}
        return make_response(jsonify(response)), 200


@blog_blueprint.route("/favorite/<int:id>", methods=["POST"])
@auth_required
def favorite(id: int, user_id: int):
    with session_db() as s:
        post = s.query(Posts).get(id)
        if not post:
            response = {"status": "fail", "message": f"Failed to Find Post: {id}"}
            return make_response(jsonify(response)), 404
        user = s.query(User).get(user_id)
        if not user:
            response = {"status": "fail", "message": f"Failed to Find User: {id}"}
            return make_response(jsonify(response)), 404
        user.favorites.append(post)
        s.commit()
        response = {"status": "success", "message": "Added post to favorites"}
        return make_response(jsonify(response)), 200


@blog_blueprint.route("/unfavorite/<int:id>", methods=["POST"])
@auth_required
def unfavorite(id: int, user_id: int):
    with session_db() as s:
        post = s.query(Posts).get(id)
        if not post:
            response = {"status": "fail", "message": f"Failed to Find Post: {id}"}
            return make_response(jsonify(response)), 404
        user = s.query(User).get(user_id)
        if not user:
            response = {"status": "fail", "message": f"Failed to Find User: {id}"}
            return make_response(jsonify(response)), 404
        user.favorites.remove(post)
        s.commit()
        response = {"status": "success", "message": "Removed post from favorites"}
        return make_response(jsonify(response)), 200


@blog_blueprint.route("/favorites", methods=["GET"])
@auth_required
def favorites(user_id: int):
    with session_db() as s:
        user = s.query(User).get(user_id)
        if not user:
            response = {"status": "fail", "message": f"Failed to Find User: {id}"}
            return make_response(jsonify(response)), 404

        posts = user.favorites
        response = {
            "status": "success",
            "message": "List of favorites posts",
            "posts": [post.serialize(user_id) for post in posts],
        }
        return make_response(jsonify(response)), 200
