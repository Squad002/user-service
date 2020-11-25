from tests.fixtures import app, client, db

from tests.helpers import user1, health_authority_not_written

from microservice.models import HealthAuthority, User

# Registration

# gli indirizzi mail sono già utilizzati, crea utenti non inseriti nel db


def test_post_should_be_successful(client, db):
    res = client.post(
        "/authorities",
        json=health_authority_not_written,
    )

    q = db.session.query(HealthAuthority).filter_by(id=3).first()

    assert res.status_code == 201
    assert q.name == health_authority_not_written["name"]
    assert q.email == health_authority_not_written["email"]
    assert q.phonenumber == health_authority_not_written["phonenumber"]
    assert q.country == health_authority_not_written["country"]
    assert q.city == health_authority_not_written["city"]
    assert q.state == health_authority_not_written["state"]
    assert q.lat == health_authority_not_written["lat"]
    assert q.lon == health_authority_not_written["lon"]


def test_post_should_be_unsuccessful(client, db):
    client.post(
        "/authorities",
        json=health_authority_not_written,
    )

    res = client.post(
        "/authorities",
        json=health_authority_not_written,
    )

    db.session.query(HealthAuthority).filter_by(id=1).first()

    assert res.status_code == 409


# Login


def test_login_should_be_successful(client):
    client.post(
        "/authorities",
        json=health_authority_not_written,
    )

    res = client.post(
        "/authorities/login",
        json={
            "email": health_authority_not_written["email"],
            "password": health_authority_not_written["password"],
        },
    )

    assert res.status_code == 200
    assert res.json["message"] == "Success"


def test_login_should_be_wrong_credentials(client):
    client.post(
        "/authorities",
        json=health_authority_not_written,
    )

    res = client.post(
        "/authorities/login",
        json={"email": health_authority_not_written["email"], "password": "wrongpass"},
    )

    assert res.status_code == 200
    assert res.json["message"] == "Wrong credentials"


def test_login_should_be_authority_not_found(client):
    res = client.post(
        "/authorities/login",
        json={
            "email": health_authority_not_written["email"],
            "password": health_authority_not_written["password"],
        },
    )

    assert res.status_code == 404
    assert res.json["message"] == "Authority not found"


# Mark


def test_should_mark_one_user_through_fiscalcode(client, db):
    res = client.post(
        "/authorities/1/mark",
        json={"identifier": user1["fiscalcode"], "duration": 15},
        follow_redirects=False,
    )

    q = User.query.filter_by(id=1).first()

    assert q.marked
    assert res.status_code == 204


def test_should_mark_one_user_through_email(client, db):
    res = client.post(
        "/authorities/1/mark",
        json={"identifier": user1["email"], "duration": 15},
        follow_redirects=False,
    )

    q = User.query.filter_by(id=1).first()

    assert q.marked
    assert res.status_code == 204


def test_should_mark_one_user_through_phonenumber(client, db):
    res = client.post(
        "/authorities/1/mark",
        json={"identifier": user1["phonenumber"], "duration": 15},
        follow_redirects=False,
    )

    q = User.query.filter_by(id=1).first()

    assert q.marked
    assert res.status_code == 204


# Trace


def test_should_trace_one_user_through_phonenumber(client, db):
    res = client.post(
        "/authorities/1/mark",
        json={"identifier": user1["phonenumber"], "duration": 15},
        follow_redirects=False,
    )

    q = User.query.filter_by(id=1).first()

    assert q.marked
    assert res.status_code == 204