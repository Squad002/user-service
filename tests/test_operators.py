from tests.fixtures import app, client, db

from microservice.models import Operator


def test_post_should_be_successful(client, db):
    res = client.post(
        "/operators",
        json=operator,
    )

    q = db.session.query(Operator).filter_by(id=1).first()

    assert res.status_code == 201
    assert q.firstname == operator["firstname"]
    assert q.lastname == operator["lastname"]
    assert q.birthdate.strftime("%Y-%m-%d") == operator["birthdate"]
    assert q.fiscalcode == operator["fiscalcode"]
    assert q.email == operator["email"]
    assert q.phonenumber == operator["phonenumber"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/operators",
        json=operator,
    )

    res = client.post(
        "/operators",
        json=operator,
    )

    db.session.query(Operator).filter_by(id=1).first()

    assert res.status_code == 409


def test_get_should_return_operator(client):
    client.post(
        "/operators",
        json=operator,
    )

    res = client.get("/operators/1")

    client.post(
        "/operators",
        json=operator,
    )

    res = client.get("/operators/1")

    assert res.status_code == 200
    assert res.json["firstname"] == operator["firstname"]
    assert res.json["lastname"] == operator["lastname"]
    assert res.json["birthdate"] == operator["birthdate"] + "T00:00:00Z"
    assert res.json["fiscalcode"] == operator["fiscalcode"]
    assert res.json["email"] == operator["email"]
    assert res.json["phonenumber"] == operator["phonenumber"]


def test_get_should_not_return_operator(client):
    res = client.get("/operators/1")

    assert res.status_code == 404

    client.post(
        "/operators",
        json=operator,
    )

    res = client.get("/operators/1")

    assert res.status_code == 200
    assert res.json["firstname"] == operator["firstname"]
    assert res.json["lastname"] == operator["lastname"]
    assert res.json["birthdate"] == operator["birthdate"] + "T00:00:00Z"
    assert res.json["fiscalcode"] == operator["fiscalcode"]
    assert res.json["email"] == operator["email"]
    assert res.json["phonenumber"] == operator["phonenumber"]


def test_patch_should_be_successful(client, db):
    client.post(
        "/operators",
        json=operator,
    )

    res = client.patch(
        "/operators/1", json={"firstname": "Giovanni", "lastname": "Verdi"}
    )
    q = db.session.query(Operator).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.firstname == "Giovanni"
    assert q.lastname == "Verdi"


def test_patch_should_not_be_successful(client):
    res = client.patch("/operators/1", json={"firstname": "Pippo"})

    assert res.status_code == 404


def test_delete_should_be_successful(client, db):
    res = client.post(
        "/operators",
        json=operator,
    )

    res = client.delete("/operators/1")

    q = db.session.query(Operator).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.firstname == ""
    assert q.lastname == ""
    assert q.fiscalcode == ""
    assert q.phonenumber == ""
    assert not q.birthdate
    assert q.email == "deleted"


def test_delete_should_not_be_successful(client):
    res = client.delete("/operators/1")

    assert res.status_code == 404


def test_login_should_be_successful(client):
    client.post(
        "/operators",
        json=operator,
    )

    res = client.post(
        "/operators/login",
        json={"email": operator["email"], "password": operator["password"]},
    )

    assert res.status_code == 200
    assert res.json["message"] == "Success"


def test_login_should_be_wrong_credentials(client):
    client.post(
        "/operators",
        json=operator,
    )

    res = client.post(
        "/operators/login", json={"email": operator["email"], "password": "wrongpass"}
    )

    assert res.status_code == 200
    assert res.json["message"] == "Wrong credentials"


def test_login_should_be_operator_not_found(client):
    res = client.post(
        "/operators/login",
        json={"email": operator["email"], "password": operator["password"]},
    )

    assert res.status_code == 404
    assert res.json["message"] == "Operator not found"


# Helpers

operator = dict(
    email="mariorossi@gmail.com",
    firstname="Mario",
    lastname="Rossi",
    password="1234",
    birthdate="1995-12-31",
    fiscalcode="RSSMRA95T31H501R",
    phonenumber="+39331303313094",
)

operator2 = dict(
    email="giovannibianchi@gmail.com",
    firstname="Mario",
    lastname="Bianchi",
    password="5678",
    birthdate="1995-01-01",
    fiscalcode="BNCGNN95T31H501R",
    phonenumber="+39 331303313095",
)
