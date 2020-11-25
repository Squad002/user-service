from microservice import db
from microservice.models import HealthAuthority, User, Operator
from microservice import client
from connexion import request
from flask import Response
from sqlalchemy import or_
from datetime import datetime, timedelta
from json import dumps

from config import (
    mail_body_covid_19_contact,
    mail_body_covid_19_mark,
    mail_body_covid_19_operator_alert,
    mail_body_covid_19_operator_booking_alert,
)


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


def mark(id):
    request.get_data()
    identifier = request.json["identifier"]
    duration = request.json["duration"]

    user_to_mark = User.query.filter(
        or_(
            User.fiscalcode.like(identifier),
            User.email.like(identifier),
            User.phonenumber.like(identifier),
        )
    ).first()

    if user_to_mark:
        authority = HealthAuthority.query.filter_by(id=id).first()
        # ok 200 Todo check if marked else "already", 200

        if user_to_mark.marked:
            pass  # TODO
        else:
            mark_helper(authority, user_to_mark, duration, datetime.utcnow())
            return Response(status=204, mimetype="application/json")
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


def mark_helper(current_authority, user, duration, starting_date):
    current_authority.mark(user, duration, starting_date=starting_date)  # todo
    db.session.commit()
    client.send_email(
        "You are positive to COVID-19",
        [user.email],
        mail_body_covid_19_mark.format(
            user.firstname,
            starting_date.strftime("%A %d. %B %Y"),
            current_authority.name,
        ),
    )
    trace_contacts(user, duration, send_email=False)  # todo set to true


def trace_contacts(user, interval, send_email=False):
    contacts = []
    if user.marked:
        user_bookings = client.get_bookings_by_user_id(user.id)

        # Get all the starting bookings, from today to "interval" days ago
        today = datetime.utcnow()
        user_bookings = list(
            filter(
                lambda x: datetime.strptime(x["start_booking"], "%Y-%m-%d %H:%M")
                >= (today - timedelta(days=interval)),
                user_bookings,
            )
        )

        for user_booking in user_bookings:
            contacts_temp = []
            starting_time = datetime.strptime(
                user_booking["start_booking"], "%Y-%m-%d %H:%M"
            )
            restaurant = client.get_restaurant_by_id(user_booking["restaurant_id"])
            operator = (
                db.session.query(Operator).filter_by(restaurant["operator_id"]).first()
            )

            if user_booking["checking"]:
                # Alert the operator about covid-positive people that had a booking in the past
                if send_email:
                    client.send_email(
                        f"You had a COVID-19 positive case in your restaurant {restaurant['name']}",
                        [operator.email],
                        mail_body_covid_19_operator_alert.format(
                            operator.firstname,
                            starting_time.strftime("%A %d. %B %Y"),
                            restaurant["name"],
                        ),
                    )

                # Check for possible contacts with other people

                # Get all the bookings that were confirmed starting from a specific time (starting_time)
                restaurant_bookings = client.get_bookings_by_restaurant_id(
                    restaurant["id"]
                )

                real_bookings = []
                tables = client.get_tables_by_restaurant_id(restaurant["id"])
                for table in tables:
                    bookings = []

                    table_bookings = client.get_bookings_by_table_id(table["id"])
                    for b in table_bookings:
                        if (
                            b["checking"]
                            and datetime.strptime(b["start_booking"], "%Y-%m-%d %H:%M")
                            == starting_time
                        ):
                            bookings.append(b)

                    real_bookings.extend(bookings)

                # Check if the users of the real bookings were having a meal during the same time of the marked user
                for b in restaurant_bookings:
                    if b["user_id"] != user.id:
                        contact = User.query.filter_by(id=b["user_id"])
                        contacts_temp.append(contact)

                        # Alert only the people that are not marked about the possible contact
                        if not contact.marked and send_email:
                            client.send_email(
                                "Possible contact with a COVID-19 positive case",
                                [contact.email],
                                mail_body_covid_19_contact.format(
                                    contact.firstname,
                                    starting_time.strftime("%A %d. %B %Y"),
                                    restaurant["name"],
                                ),
                            )

                if contacts_temp:
                    contacts.append({"date": starting_time, "people": contacts_temp})
            elif starting_time >= datetime.utcnow() and send_email:
                # Alert the operator about the future booking
                table = client.get_table_by_id(user_booking["table_id"])

                client.send_email(
                    f"You have a booking of a COVID-19 positive case in your restaurant {restaurant.name}",
                    [operator.email],
                    mail_body_covid_19_operator_booking_alert.format(
                        operator.firstname,
                        restaurant["name"],
                        user_booking["booking_number"],
                        table["name"],
                    ),
                )

    return contacts
