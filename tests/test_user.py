from src.models.models import session_db, User, Posts, Group, user_group
import time
import requests


def test_create_user(app):
    with app.app_context():
        with session_db() as s:
            new_user = User(name="a", password="a")
            s.add(new_user)
            s.commit()
            query = (
                s.query(User)
                .filter(User.name == new_user.name, User.password == new_user.password)
                .first()
            )
            assert query == new_user
            s.query(User).filter(
                User.name == new_user.name, User.password == new_user.password
            ).delete()
            s.commit()


def test_register_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/register",
        json={"username": "joe@gmail.com", "password": "123456", "groups": [1, 2]},
    )
    expected_response = {
        "status": "success",
        "message": "Successfully registered. Please Login",
    }
    assert resp.json() == expected_response


def test_delete_of_exiting_user():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/delete",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    expected_response = {"status": "success", "message": "Successfully deleted user."}
    assert resp.json() == expected_response


def test_register_with_empty_username():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/register",
        json={"username": "", "password": "123456", "groups": [1, 2]},
    )
    expected_response = {"status": "fail", "message": "Username is required."}

    print(resp.json())
    assert resp.json() == expected_response


def test_register_with_empty_password():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/register",
        json={"username": "joe", "password": "", "groups": [1, 2]},
    )
    expected_response = {"status": "fail", "message": "Password is required."}
    assert resp.json() == expected_response


def test_register_without_groups():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/register",
        json={"username": "joe1@gmail.com", "password": "123456"},
    )
    expected_response = {
        "status": "fail",
        "message": "Groups are required. Submit at least empty list",
    }
    assert resp.json() == expected_response


def test_register_with_no_password():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/register",
        json={"username": "joe@gmail.com", "assword": "123456", "groups": [1, 2]},
    )
    expected_response = {"status": "fail", "message": "Password is required."}
    assert resp.json() == expected_response


def test_login_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "q", "password": "q"},
    )
    responseObject = {"status": "success", "message": "Successfully logged in."}
    assert resp.json().get("status") == "success"


def test_logout_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "q", "password": "q"},
    )
    token = resp.json()["auth_token"]
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/logout",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["status"] == "success"


def test_logout_with_invalid_header():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "q", "password": "q"},
    )
    token = resp.json()["auth_token"]
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/logout",
        headers={"Authorizatioa": f"{token}"},
    )
    assert resp.json()["message"] == "Missing Authorization Header"


def test_logout_with_invalid_token():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "q", "password": "q"},
    )
    token = resp.json()["auth_token"]
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/logout",
        headers={"Authorization": f"aasdqwdasdasd"},
    )
    assert resp.json()["message"] == "Invalid token. Please log in again."


def test_logout_with_timed_out_token():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "q", "password": "q"},
    )
    token = resp.json()["auth_token"]
    time.sleep(6)
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/logout",
        headers={"Authorization": f"{token}"},
    )
    assert resp.json()["message"] == "Signature expired. Please log in again."


def test_login_with_invalid_username():
    resp = requests.post(
        url="http://127.0.0.1:8000/api/auth/login",
        json={"username": "qqw", "password": "q"},
    )
    assert resp.json().get("message") == "User/Password incorrect. Please try again."
