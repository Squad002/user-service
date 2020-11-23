from microservice import db
from microservice.models import User
from flask import Response
from flask.json import dumps
from connexion import request
from datetime import datetime


def search():
    request.get_data()
    req_data = request.args

    query = db.session.query(User)
    for attr, value in req_data.items():
        query = query.filter(getattr(User, attr) == value)

    users = dumps(
        [
            user.serialize(
                [
                    "id",
                    "firstname",
                    "lastname",
                    "email",
                    "fiscalcode",
                    "phonenumber",
                    "birthdate",
                    "marked",
                    "is_registered",
                ]
            )
            for user in query.all()
        ]
    )

    return Response(users, status=200, mimetype="application/json")


def post():
    request.get_data()
    user = request.json

    new_user = db.session.query(User.id).filter_by(email=user["email"]).first()
    if not new_user:
        new_user = User(
            firstname=user["firstname"],
            lastname=user["lastname"],
            email=user["email"],
            password=user["password"],
            birthdate=datetime.strptime(user["birthdate"], "%Y-%m-%d"),
            phonenumber=user["phonenumber"],
            fiscalcode=user["fiscalcode"],
        )

        db.session.add(new_user)
        db.session.commit()
        return Response(status=201)

    return Response(status=409)


def get(id):
    user = db.session.query(User).filter_by(id=id).first()

    if user:
        return Response(
            dumps(
                user.serialize(
                    [
                        "id",
                        "firstname",
                        "lastname",
                        "email",
                        "fiscalcode",
                        "phonenumber",
                        "birthdate",
                        "marked",
                    ]
                )
            ),
            status=200,
            mimetype="application/json",
        )

    return Response(status=404)


def patch(id):
    user = db.session.query(User).filter_by(id=id).first()

    if user:
        request.get_data()
        new_user = request.json

        for k, v in new_user.items():
            setattr(user, k, v)

        db.session.commit()
        return Response(status=204)

    return Response(status=404)


def delete(id):
    user = db.session.query(User).filter(User.id == id, User.email != "deleted").first()

    if user:
        (
            user.firstname,
            user.lastname,
            user.password_hash,
            user.fiscalcode,
            user.phonenumber,
            user.birthdate,
            user.email,
        ) = ("", "", "", "", "", None, "deleted")
        db.session.commit()
        return Response(status=204)

    return Response(status=404)


def login():
    request.get_data()
    user = request.json

    email = user["email"]
    password = user["password"]

    user = db.session.query(User).filter_by(email=email).first()
    if user:
        message = "Success" if user.verify_password(password) else "Wrong credentials"
        return Response(
            dumps({"message": message}), status=200, mimetype="application/json"
        )
    else:
        return Response(
            dumps({"message": "User not found"}),
            status=404,
            mimetype="application/json",
        )
