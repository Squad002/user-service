from microservice import db
from microservice.models import HealthAuthority, User
from connexion import request
from flask import Response
from sqlalchemy import or_
from datetime import datetime
from json import dumps


def get():
    pass


def search():
    request.get_data()
    req_data = request.args

    query = db.session.query(HealthAuthority)
    for attr, value in req_data.items():
        query = query.filter(getattr(HealthAuthority, attr) == value)

    authorities = dumps(
        [
            authorities.serialize(
                [
                    "id",
                    "name",
                    "email",
                    "fiscalcode",
                    "phonenumber",
                    "country",
                    "state",
                    "city",
                    "lat",
                    "lon",
                    "is_registered",
                ]
            )
            for authorities in query.all()
        ]
    )

    return Response(authorities, status=200, mimetype="application/json")


def mark(authority_id):
    request.get_data()
    identifier = request.json["identifier"]
    duration = request.json["duration"]

    user_to_mark = User.query.filter(
        or_(
            User.fiscal_code.like(identifier),
            User.email.like(identifier),
            User.phone_number.like(identifier),
        )
    )

    if user_to_mark:
        authority = HealthAuthority.query.filter_by(id == authority_id)
        mark(authority, user_to_mark, duration, datetime.utcnow())
        return Response()
    else:
        return Response(status=404, mimetype="application/json")


def trace():
    pass


def post():
    request.get_data()
    authority = request.json

    new_authority = (
        db.session.query(HealthAuthority.id).filter_by(email=authority["email"]).first()
    )
    if not new_authority:
        new_authority = HealthAuthority(
            email=authority["email"],
            name=authority["name"],
            password=authority["password"],
            phonenumber=authority["phonenumber"],
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


def login():
    request.get_data()
    user = request.json

    email = user["email"]
    password = user["password"]

    user = db.session.query(HealthAuthority).filter_by(email=email).first()
    if user:
        message = "Success" if user.verify_password(password) else "Wrong credentials"
        return Response(
            dumps({"message": message}), status=200, mimetype="application/json"
        )
    else:
        return Response(
            dumps({"message": "Authority not found"}),
            status=404,
            mimetype="application/json",
        )


# def mark(current_authority, user, duration, starting_date):
#     # Authority mark user
#     current_authority.mark(user, duration, starting_date=starting_date)
#     db.session.commit()
#     tasks.send_email(
#         "You are positive to COVID-19",
#         [user.email],
#         mail_body_covid_19_mark.format(
#             user.firstname,
#             starting_date.strftime("%A %d. %B %Y"),
#             current_authority.name,
#         ),
#     )
#     trace_contacts(user, duration, send_email=True)


# def trace_contacts(user, interval, send_email=False):
#     contacts = []
#     if user.is_marked():
#         user_bookings = user.get_bookings(range_duration=interval)

#         for user_booking in user_bookings:
#             contacts_temp = []
#             starting_time = user_booking.start_booking
#             restaurant = user_booking.table.restaurant
#             operator = restaurant.operator

#             if user_booking.checkin:
#                 # Alert the operator about the past booking
#                 if send_email:
#                     tasks.send_email(
#                         f"You had a COVID-19 positive case in your restaurant {restaurant.name}",
#                         [operator.email],
#                         mail_body_covid_19_operator_alert.format(
#                             operator.firstname,
#                             starting_time.strftime("%A %d. %B %Y"),
#                             restaurant.name,
#                         ),
#                     )

#                 # Check for possible contacts with other people
#                 restaurant_bookings = restaurant.get_bookings(starting_time)
#                 for b in restaurant_bookings:
#                     if b.user != user:
#                         contacts_temp.append(b.user)
#                         if not b.user.is_marked() and send_email:
#                             # Alert only the people that are not marked about the possible contact
#                             tasks.send_email(
#                                 "Possible contact with a COVID-19 positive case",
#                                 [b.user.email],
#                                 mail_body_covid_19_contact.format(
#                                     b.user.firstname,
#                                     starting_time.strftime("%A %d. %B %Y"),
#                                     restaurant.name,
#                                 ),
#                             )

#                 if contacts_temp:
#                     contacts.append({"date": starting_time, "people": contacts_temp})
#             elif starting_time >= datetime.utcnow() and send_email:
#                 # Alert the operator about the future booking
#                 tasks.send_email(
#                     f"You have a booking of a COVID-19 positive case in your restaurant {restaurant.name}",
#                     [operator.email],
#                     mail_body_covid_19_operator_booking_alert.format(
#                         operator.firstname,
#                         restaurant.name,
#                         user_booking.id,
#                         user_booking.table.name,
#                     ),
#                 )

#     return contacts
