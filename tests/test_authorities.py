from tests.fixtures import app, client, db

from microservice.models import HealthAuthority


def test_post_should_be_successful(client, db):
    res = client.post(
        "/authorities",
        json=authority,
    )

    q = db.session.query(HealthAuthority).filter_by(id=1).first()

    assert res.status_code == 201
    assert q.name == authority["name"]
    assert q.email == authority["email"]
    assert q.phone == authority["phone"]
    assert q.country == authority["country"]
    assert q.city == authority["city"]
    assert q.state == authority["state"]
    assert q.lat == authority["lat"]
    assert q.lon == authority["lon"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/authorities",
        json=authority,
    )

    res = client.post(
        "/authorities",
        json=authority,
    )

    db.session.query(HealthAuthority).filter_by(id=1).first()

    assert res.status_code == 409


def test_login_should_be_successful(client):
    client.post(
        "/authorities",
        json=authority,
    )

    res = client.post(
        "/authorities/login",
        json={"email": authority["email"], "password": authority["password"]},
    )

    assert res.status_code == 200
    assert res.json["message"] == "Success"


def test_login_should_be_wrong_credentials(client):
    client.post(
        "/authorities",
        json=authority,
    )

    res = client.post(
        "/authorities/login",
        json={"email": authority["email"], "password": "wrongpass"},
    )

    assert res.status_code == 200
    assert res.json["message"] == "Wrong credentials"


def test_login_should_be_authority_not_found(client):
    res = client.post(
        "/authorities/login",
        json={"email": authority["email"], "password": authority["password"]},
    )

    assert res.status_code == 404
    assert res.json["message"] == "Authority not found"


# Helpers

authority = {
    "email": "authority@gmail.com",
    "name": "ASL Pisa",
    "password": "password",
    "phone": "+39 33133133130",
    "country": "Italy",
    "state": "Tuscany",
    "city": "Pisa",
    "lat": 324234.32,
    "lon": 324234.32,
}
