from microservice import db
from microservice.models import HealthAuthority
from connexion import request
from flask import Response

def mark():
    pass


def trace():
    pass


def post():
    request.get_data()
    authority = request.json

    new_authority = db.session.query(HealthAuthority.id).filter_by(email=authority["email"]).first()
    if not new_authority:
        new_authority = HealthAuthority(
            email=authority["email"],
            name=authority["name"],
            password=authority["password"],
            phone=authority["phone"],
            country=authority["country"],
            state=authority["state"],
            city=authority["city"],
            lat=authority["lat"],
            lon=authority["lon"],
        )

        db.session.add(new_authority)
        db.session.commit()
        return Response(status=201)

    return Response(status=409)


def get():
    pass


def prova():
    pass