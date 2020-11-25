from tests.fixtures import app, client, db
from tests.helpers import user1, user_not_written

from microservice.models import User


def test_search_should_return_results(client):
    res = client.get("/users?firstname=Mario")

    assert res.status_code == 200
    assert res.json[0]["firstname"] == user1["firstname"]
    assert res.json[1]["firstname"] == user1["firstname"]


def test_search_should_return_empty_results(client):
    res = client.get("/users?firstname=Marioz")

    assert res.status_code == 200
    assert res.json == []


def test_post_should_be_successful(client, db):
    res = client.post("/users", json=user_not_written)

    q = db.session.query(User).filter_by(id=7).first()

    assert res.status_code == 201
    assert q.firstname == user_not_written["firstname"]
    assert q.lastname == user_not_written["lastname"]
    assert q.birthdate.strftime("%Y-%m-%d") == user_not_written["birthdate"].strftime(
        "%Y-%m-%d"
    )
    assert q.fiscalcode == user_not_written["fiscalcode"]
    assert q.email == user_not_written["email"]
    assert q.phonenumber == user_not_written["phonenumber"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/users",
        json=user_not_written,
    )

    res = client.post(
        "/users",
        json=user_not_written,
    )

    db.session.query(User).filter_by(id=1).first()

    assert res.status_code == 409


def test_put_should_be_successful(client, db):
    user_not_written.pop("password")
    user_not_written.pop("phonenumber")
    user_not_written.pop("birthdate")

    res = client.put("/users", json=user_not_written)

    q = db.session.query(User).filter_by(id=7).first()

    assert res.status_code == 204
    assert q.firstname == user_not_written["firstname"]
    assert q.lastname == user_not_written["lastname"]
    assert q.fiscalcode == user_not_written["fiscalcode"]
    assert q.email == user_not_written["email"]


def test_get_should_return_user(client):
    res = client.get("/users/1")

    assert res.status_code == 200
    assert res.json["firstname"] == user1["firstname"]
    assert res.json["lastname"] == user1["lastname"]
    assert res.json["birthdate"] == user1["birthdate"].strftime("%Y-%m-%d")
    assert res.json["fiscalcode"] == user1["fiscalcode"]
    assert res.json["email"] == user1["email"]
    assert res.json["phonenumber"] == user1["phonenumber"]


def test_get_should_not_return_user(client):
    res = client.get("/users/10")

    assert res.status_code == 404


def test_patch_should_be_successful(client, db):
    client.post(
        "/users",
        json=user1,
    )

    res = client.patch("/users/1", json={"firstname": "Giovanni", "lastname": "Verdi"})
    q = db.session.query(User).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.firstname == "Giovanni"
    assert q.lastname == "Verdi"


def test_patch_should_not_be_successful(client):
    res = client.patch("/users/10", json={"firstname": "Pippo"})

    assert res.status_code == 404


def test_delete_should_be_successful(client, db):
    res = client.post(
        "/users",
        json=user1,
    )

    res = client.delete("/users/1")

    q = db.session.query(User).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.firstname == ""
    assert q.lastname == ""
    assert q.fiscalcode == ""
    assert q.phonenumber == ""
    assert not q.birthdate
    assert q.email == "deleted"


def test_delete_should_not_be_successful(client):
    res = client.delete("/users/10")

    assert res.status_code == 404


def test_login_should_be_successful(client):
    client.post(
        "/users",
        json=user1,
    )

    res = client.post(
        "/users/login", json={"email": user1["email"], "password": user1["password"]}
    )

    assert res.status_code == 200
    assert res.json["message"] == "Success"


def test_login_should_be_wrong_credentials(client):
    client.post(
        "/users",
        json=user1,
    )

    res = client.post(
        "/users/login", json={"email": user1["email"], "password": "wrongpass"}
    )

    assert res.status_code == 200
    assert res.json["message"] == "Wrong credentials"


def test_login_should_be_user_not_found(client):
    res = client.post(
        "/users/login",
        json={
            "email": "thisdoesnotexist",
            "password": "prova",
        },
    )

    assert res.status_code == 404
    assert res.json["message"] == "User not found"
