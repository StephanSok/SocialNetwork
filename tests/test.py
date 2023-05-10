from starlette.testclient import TestClient
from backend.routers.auth import create_access_token
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/user/users")
    assert response.status_code == 404
    assert response.json() == {"detail": "Users not found"}


def test_user_create():
    content = (
        'username=name1&info=cool&age=15&email=test%40gmail.com&password=1'
    )

    response = client.post(
        "/user/create",
        data=content,
        headers={
            'accept': 'application/json',
            "content-type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    assert response.json() == 1


def test_get_users():
    list_users: dict = {
        "1": {
            "name": "name1",
            "info": "cool",
            "age": 15,
            "email": "test@gmail.com",
            "friends": [],
        },
        "2": {
            "name": "name2",
            "info": "cool",
            "age": 15,
            "email": "test@gmail.com",
            "friends": [],
        },
        "3": {
            "name": "name3",
            "info": "cool",
            "age": 15,
            "email": "test@gmail.com",
            "friends": [],
        },
    }
    content = (
        'username=name2&info=cool&age=15&email=test%40gmail.com&password=1'
    )
    response = client.post(
        "/user/create",
        data=content,
        headers={
            'accept': 'application/json',
            "content-type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    assert response.json() == 2
    content = (
        'username=name3&info=cool&age=15&email=test%40gmail.com&password=1'
    )
    response = client.post(
        "/user/create",
        data=content,
        headers={
            'accept': 'application/json',
            "content-type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 200
    assert response.json() == 3
    response = client.get("/user/users")
    assert response.status_code == 200
    assert response.json() == list_users


def test_get_user():
    response = client.get("/user/2")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_user_with_jwt():
    token = "Bearer " + create_access_token({"id": 2})
    response = client.get("/user/2", headers={'Authorization': token})
    assert response.status_code == 200
    assert response.json() == {
        "name": "name2",
        "info": "cool",
        "age": 15,
        "email": "test@gmail.com",
        "friends": [],
    }


def test_make_friends():
    token = "Bearer " + create_access_token({"id": 1})
    response = client.post(
        "/user/friend",
        data='id1=1&id2=2',
        headers={
            'Authorization': token,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}


def test_make_friends_again():
    token = "Bearer " + create_access_token({"id": 1})
    response = client.post(
        "/user/friend",
        data='id1=1&id2=2',
        headers={
            'Authorization': token,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Already friends"}


def edit_user():
    token = "Bearer " + create_access_token({"id": 2})
    response = client.post(
        "/user/edit/1",
        data={"age": 1337, "email": "cool@mail.com"},
        headers={
            'Content-Type': 'application/json',
            'Authorization': token,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}


def test_chat():
    token = "Bearer " + create_access_token({"id": 1})
    response = client.get("/chat/1/3", headers={'Authorization': token})
    assert response.status_code == 404
    assert response.json() == {"detail": "No access to chat"}


def test_chat_with_friend():
    token = "Bearer " + create_access_token({"id": 1})
    response = client.get("/chat/1/2", headers={'Authorization': token})
    assert response.status_code == 200
