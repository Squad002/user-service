from tests.fixtures import app, client, db

from microservice.models import User


def test_search_should_return_results(client):
    client.post(
        "/users",
        json=user,
    )

    client.post(
        "/users",
        json=user2,
    )

    res = client.get("/users?firstname=Mario")

    assert res.status_code == 200
    assert res.json[0]["firstname"] == user["firstname"]
    assert res.json[1]["firstname"] == user["firstname"]


def test_search_should_return_empty_results(client):
    client.post(
        "/users",
        json=user,
    )

    client.post(
        "/users",
        json=user2,
    )

    res = client.get("/users?firstname=Marioz")

    assert res.status_code == 200
    assert res.json == []


def test_post_should_be_successful(client, db):
    res = client.post(
        "/users",
        json=user,
    )

    q = db.session.query(User).filter_by(id=1).first()

    assert res.status_code == 201
    assert q.firstname == user["firstname"]
    assert q.lastname == user["lastname"]
    assert q.birthdate.strftime("%Y-%m-%d") == user["birthdate"]
    assert q.fiscalcode == user["fiscalcode"]
    assert q.email == user["email"]
    assert q.phonenumber == user["phonenumber"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/users",
        json=user,
    )

    res = client.post(
        "/users",
        json=user,
    )

    db.session.query(User).filter_by(id=1).first()

    assert res.status_code == 409


def test_get_should_return_user(client):
    client.post(
        "/users",
        json=user,
    )

    res = client.get("/users/1")

    client.post(
        "/users",
        json=user,
    )

    res = client.get("/users/1")

    assert res.status_code == 200
    assert res.json["firstname"] == user["firstname"]
    assert res.json["lastname"] == user["lastname"]
    assert res.json["birthdate"] == user["birthdate"] + "T00:00:00Z"
    assert res.json["fiscalcode"] == user["fiscalcode"]
    assert res.json["email"] == user["email"]
    assert res.json["phonenumber"] == user["phonenumber"]


def test_get_should_not_return_user(client):
    res = client.get("/users/1")

    assert res.status_code == 404

    client.post(
        "/users",
        json=user,
    )

    res = client.get("/users/1")

    assert res.status_code == 200
    assert res.json["firstname"] == user["firstname"]
    assert res.json["lastname"] == user["lastname"]
    assert res.json["birthdate"] == user["birthdate"] + "T00:00:00Z"
    assert res.json["fiscalcode"] == user["fiscalcode"]
    assert res.json["email"] == user["email"]
    assert res.json["phonenumber"] == user["phonenumber"]


def test_patch_should_be_successful(client, db):
    client.post(
        "/users",
        json=user,
    )

    res = client.patch("/users/1", json={"firstname": "Giovanni", "lastname": "Verdi"})
    q = db.session.query(User).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.firstname == "Giovanni"
    assert q.lastname == "Verdi"


def test_patch_should_not_be_successful(client):
    res = client.patch("/users/1", json={"firstname": "Pippo"})

    assert res.status_code == 404


def test_delete_should_be_successful(client, db):
    res = client.post(
        "/users",
        json=user,
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
    res = client.delete("/users/1")

    assert res.status_code == 404


def test_login_should_be_successful(client):
    client.post(
        "/users",
        json=user,
    )

    res = client.post(
        "/users/login", json={"email": user["email"], "password": user["password"]}
    )

    assert res.status_code == 200
    assert res.json["message"] == "Success"


def test_login_should_be_wrong_credentials(client):
    client.post(
        "/users",
        json=user,
    )

    res = client.post(
        "/users/login", json={"email": user["email"], "password": "wrongpass"}
    )

    assert res.status_code == 200
    assert res.json["message"] == "Wrong credentials"


def test_login_should_be_user_not_found(client):
    res = client.post(
        "/users/login", json={"email": user["email"], "password": user["password"]}
    )

    assert res.status_code == 404
    assert res.json["message"] == "User not found"


# Helpers

user = dict(
    email="mariorossi@gmail.com",
    firstname="Mario",
    lastname="Rossi",
    password="1234",
    birthdate="1995-12-31",
    fiscalcode="RSSMRA95T31H501R",
    phonenumber="+39331303313094",
)

user2 = dict(
    email="giovannibianchi@gmail.com",
    firstname="Mario",
    lastname="Bianchi",
    password="5678",
    birthdate="1995-01-01",
    fiscalcode="BNCGNN95T31H501R",
    phonenumber="+39 331303313095",
)
