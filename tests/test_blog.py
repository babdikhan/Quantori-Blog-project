from src.models.models import session_db, User, Posts, Group, user_group
from flask import session

import requests
import time


def test_create_post(app):
    with app.app_context():
        with session_db() as s:
            new_post = Posts(title="title", body="body", user_id=1)
            s.add(new_post)
            s.commit()
            assert True == True


def test_update_post(app):
    with app.app_context():
        with session_db() as s:
            post = s.query(Posts).get(49)
            post.title = "title"
            post.body = "body"

            s.commit()
            assert True == True


def test_delete_post(app):
    with app.app_context():
        with session_db() as s:
            post = s.query(Posts).filter(Posts.id == 49).delete()

            s.commit()
            assert True == True


def test_index_with_valid_data(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["status"] == "success"


def test_index_without_token(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorizaon": f"{token}"},
    )
    assert resp.json()["message"] == "Missing Authorization Header"


def test_index_with_invalid_token(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"safqwdasdw"},
    )
    assert resp.json()["message"] == "Invalid token. Please log in again."


def test_create_with_valid_data(token):
    resp = requests.post(
        url="http://127.0.0.1:8000/api/post/create",
        json={"title": "API 1 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["status"] == "success"


def test_create_without_title(token):
    resp = requests.post(
        url="http://127.0.0.1:8000/api/post/create",
        json={"ti": "API 1 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Title is required."


def test_create_without_body(token):
    resp = requests.post(
        url="http://127.0.0.1:8000/api/post/create",
        json={"title": "API 1 title", "bdy": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Body is required."


def test_create_with_empty_body(token):
    resp = requests.post(
        url="http://127.0.0.1:8000/api/post/create",
        json={"title": "API 1 title", "body": ""},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Body is required."


def test_create_with_empty_title(token):
    resp = requests.post(
        url="http://127.0.0.1:8000/api/post/create",
        json={"title": "", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Title is required."


def test_update_with_valid_data(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    posts = resp.json()["posts"]

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/update/{posts[0]['id']}",
        json={"title": "API 2 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Post updated"


def test_update_with_invalid_post_id(token):
    post_id = "21335"
    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/update/{post_id}",
        json={"title": "API 2 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == f"Failed to Find Post: {post_id}"


def test_update_someone_else_post(token):
    """
    this test might fail due to hard coded values. for now its not possible to pass to the test
    information about the ownership of posts
    """
    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/update/{63}",
        json={"title": "API 2 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Can't edit someone else's post"


def test_delete_with_valid_data(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    posts = resp.json()["posts"]

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/delete/{posts[0]['id']}",
        json={"title": "API 2 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Post deleted"


def test_delete_with_invalid_token_id(token):
    post_id = "12323123"

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/delete/{post_id}",
        json={"title": "API 2 title", "body": "API 1 Body"},
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == f"Failed to Find Post: {post_id}"


def test_favorite_with_valid_data(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    posts = resp.json()["posts"]

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/favorite/{posts[0]['id']}",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Added post to favorites"


def test_favorite_with_invalid_post_id(token):
    post_id = "123123123"

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/favorite/{post_id}",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == f"Failed to Find Post: {post_id}"


def test_index_favorites_with_valid_data(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/favorites",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "List of favorites posts"


def test_unfavorite_with_valid_data(token):
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/favorites",
        headers={"Authorization": f"{token}"},
    )
    favorites = resp.json()["posts"]

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/unfavorite/{favorites[0]['id']}",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Removed post from favorites"


def test_unfavorite_with_invalid_post_id(token):
    post_id = "123123123"

    resp = requests.post(
        url=f"http://127.0.0.1:8000/api/post/unfavorite/{post_id}",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == f"Failed to Find Post: {post_id}"


def test_index_with_old_token(token):
    time.sleep(6)
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Signature expired. Please log in again."


def test_index_with_blacklisted_token(token):
    requests.post(
        url="http://127.0.0.1:8000/api/auth/logout",
        headers={"Authorization": f"{token}"},
    )
    resp = requests.get(
        url="http://127.0.0.1:8000/api/post/",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Token Blacklisted"
