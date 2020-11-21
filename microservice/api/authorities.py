from microservice import db
from microservice.models import HealthAuthority, User
from connexion import request
from flask import Response

def mark():
    request.get_data()
    identification = request.json
    if identification["phone"]:
        user = db.session.query(User).filter_by(phone=identification["phone"]).first()
    elif identification["fiscalcode"]:
        user = db.session.query(User).filter_by(fiscalcode=identification["fiscalcode"]).first()
    elif identification["email"]:
        user = db.session.query(User).filter_by(email=identification["email"]).first()
    
    # user.mark?? come lo implementiamo?

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