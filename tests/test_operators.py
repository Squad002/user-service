from tests.fixtures import app, client, db
from tests.helpers import operator_not_written

from microservice.models import Operator


def test_post_should_be_successful(client, db):
    res = client.post(
        "/operators",
        json=operator_not_written,
    )

    q = db.session.query(Operator).filter_by(id=3).first()

    assert res.status_code == 201
    assert q.firstname == operator_not_written["firstname"]
    assert q.lastname == operator_not_written["lastname"]
    assert q.birthdate.strftime("%Y-%m-%d") == operator_not_written[
        "birthdate"
    ].strftime("%Y-%m-%d")
    assert q.fiscalcode == operator_not_written["fiscalcode"]
    assert q.email == operator_not_written["email"]
    assert q.phonenumber == operator_not_written["phonenumber"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/operators",
        json=operator_not_written,
    )

    res = client.post(
        "/operators",
        json=operator_not_written,
    )

    db.session.query(Operator).filter_by(id=1).first()

    assert res.status_code == 409


def test_get_should_return_operator(client):
    client.post(
        "/operators",
        json=operator_not_written,
    )

    res = client.get("/operators/3")

    assert res.status_code == 200
    assert res.json["firstname"] == operator_not_written["firstname"]
    assert res.json["lastname"] == operator_not_written["lastname"]
    assert res.json["birthdate"] == operator_not_written["birthdate"].strftime(
        "%Y-%m-%d"
    )
    assert res.json["fiscalcode"] == operator_not_written["fiscalcode"]
    assert res.json["email"] == operator_not_written["email"]
    assert res.json["phonenumber"] == operator_not_written["phonenumber"]


def test_get_should_not_return_operator(client):
    res = client.get("/operators/3")

    assert res.status_code == 404

    client.post(
        "/operators",
        json=operator_not_written,
    )

    res = client.get("/operators/3")

    assert res.status_code == 200
    assert res.json["firstname"] == operator_not_written["firstname"]
    assert res.json["lastname"] == operator_not_written["lastname"]
    assert res.json["birthdate"] == operator_not_written["birthdate"].strftime(
        "%Y-%m-%d"
    )
    assert res.json["fiscalcode"] == operator_not_written["fiscalcode"]
    assert res.json["email"] == operator_not_written["email"]
    assert res.json["phonenumber"] == operator_not_written["phonenumber"]


def test_patch_should_be_successful(client, db):
    client.post(
        "/operators",
        json=operator_not_written,
    )

    res = client.patch(
        "/operators/1", json={"firstname": "Giovanni", "lastname": "Verdi"}
    )
    q = db.session.query(Operator).filter_by(id=1).first()

    assert res.status_code == 204
    assert q.firstname == "Giovanni"
    assert q.lastname == "Verdi"


def test_patch_should_not_be_successful(client):
    res = client.patch("/operators/3", json={"firstname": "Pippo"})

    assert res.status_code == 404


def test_delete_should_be_successful(client, db):
    res = client.post(
        "/operators",
        json=operator_not_written,
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
    res = client.delete("/operators/4")

    assert res.status_code == 404


def test_login_should_be_successful(client):
    client.post(
        "/operators",
        json=operator_not_written,
    )

    res = client.post(
        "/operators/login",
        json={
            "email": operator_not_written["email"],
            "password": operator_not_written["password"],
        },
    )

    assert res.status_code == 200
    assert res.json["message"] == "Success"


def test_login_should_be_wrong_credentials(client):
    client.post(
        "/operators",
        json=operator_not_written,
    )

    res = client.post(
        "/operators/login",
        json={"email": operator_not_written["email"], "password": "wrongpass"},
    )

    assert res.status_code == 200
    assert res.json["message"] == "Wrong credentials"


def test_login_should_be_operator_not_found(client):
    res = client.post(
        "/operators/login",
        json={
            "email": operator_not_written["email"],
            "password": operator_not_written["password"],
        },
    )

    assert res.status_code == 404
    assert res.json["message"] == "Operator not found"
