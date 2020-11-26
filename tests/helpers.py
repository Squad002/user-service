# Methods
from flask import current_app
from microservice.models import User, HealthAuthority, Operator, Mark
from microservice import db

import requests

from datetime import date, datetime, time, timedelta

# Methods


def generate_all():
    global user1, user2, user3, user4, user5, user6
    global operator1, operator2
    global health_authority1, health_authority2, mark
    global restaurant1, table1, table2, table3
    global booking1, booking2, booking2_confirm, booking3, booking4, booking5
    global checkin1, checkin2, checkin4, checkin5

    user1db = User(**user1)
    user2db = User(**user2)
    user3db = User(**user3)
    user4db = User(**user4)
    user5db = User(**user5)
    user6db = User(**user6)
    db.session.add(user1db)
    db.session.add(user2db)
    db.session.add(user3db)
    db.session.add(user4db)
    db.session.add(user5db)
    db.session.add(user6db)

    operator1db = Operator(**operator1)
    operator2db = Operator(**operator2)
    db.session.add(operator1db)
    db.session.add(operator2db)
    db.session.commit()

    health_authority1db = HealthAuthority(**health_authority1)
    health_authority2db = HealthAuthority(**health_authority2)
    markdb = Mark(**mark)
    db.session.add(health_authority1db)
    db.session.add(health_authority2db)
    db.session.add(markdb)
    db.session.commit()

    # Restaurants and tables
    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}restaurants",
        json=restaurant1,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}tables",
        json=table1,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}tables",
        json=table2,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}tables",
        json=table3,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}tables",
        json=table4,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}tables",
        json=table5,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_RESTAURANT']}tables",
        json=table6,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    # Booking and checkins
    requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings",
        json=booking1,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings",
        json=booking2,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_BOOKING']}booking/confirm",
        json=booking2_confirm,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings",
        json=booking3,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings",
        json=booking4,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )
    requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings",
        json=booking5,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    requests.post(
        f"{current_app.config['URL_API_BOOKING']}reservations/checkin",
        json=checkin1,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    requests.post(
        f"{current_app.config['URL_API_BOOKING']}reservations/checkin",
        json=checkin2,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    requests.post(
        f"{current_app.config['URL_API_BOOKING']}reservations/checkin",
        json=checkin4,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    requests.post(
        f"{current_app.config['URL_API_BOOKING']}reservations/checkin",
        json=checkin5,
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )


# Data

user1 = dict(
    email="mariobrown@gmail.com",
    firstname="Mario",
    lastname="Brown",
    password="1234",
    birthdate=date(1995, 12, 31),
    fiscalcode="RSSMRA95T31H501R",
    phonenumber="+39331303313094",
)

user2 = dict(
    email="mariogreen@gmail.com",
    firstname="Mario",
    lastname="Green",
    password="1234",
    birthdate=date(1995, 12, 31),
    fiscalcode="GREMRA95T31H501R",
    phonenumber="+39331303313095",
)


user3 = dict(
    email="giovanniyellow@gmail.com",
    firstname="Giovanni",
    lastname="Yellow",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="RSSGVA95T31J591K",
    phonenumber="+39334334683094",
)

user4 = dict(
    email="carmeloosvaldino@gmail.com",
    firstname="carmelo",
    lastname="osvaldino",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="OSVCAR95T31J591K",
    phonenumber="+39334334683456",
)

user5 = dict(
    email="johonnymarsiglia@gmail.com",
    firstname="johnny",
    lastname="marsiglia",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="MRGJHN95T31J591K",
    phonenumber="+39334554683094",
)

user6 = dict(
    email="annacavatello@lalocanda.com",
    firstname="anna",
    lastname="cavatello",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="CVTANN63A01B519O",
    phonenumber="+3933456346094",
)

user_not_written = dict(
    email="osvaldopaniccia@panicone.com",
    firstname="osvaldo",
    lastname="paniccia",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="PNCOSV63A01B519O",
    phonenumber="+393345634444",
)

operator1 = dict(
    email="giuseppebrown@lalocanda.com",
    firstname="giuseppe",
    lastname="yellow",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="YLLGPP63A01B519O",
    phonenumber="+39331303313094",
)

operator2 = dict(
    email="giovannibianchi@archetto.com",
    firstname="Mario",
    lastname="Bianchi",
    password="5678",
    birthdate=date(1995, 1, 1),
    fiscalcode="BNCGNN95T31H501R",
    phonenumber="+39 331303313095",
)

operator_not_written = dict(
    email="osvaldopaniccia@dapaniccia.com",
    firstname="osvaldo",
    lastname="paniccia",
    password="5678",
    birthdate=date(1995, 12, 31),
    fiscalcode="PNCOSV63A01B519O",
    phonenumber="+393345634444",
)

health_authority1 = dict(
    email="canicatti@asl.it",
    name="ASL Canicattì",
    password="cani123",
    phonenumber="0808403849",
    country="Italy",
    state="AG",
    city="Canicattì",
    lat=37.36,
    lon=13.84,
)

health_authority2 = dict(
    email="roma@asl.it",
    name="ASL Roma",
    password="romasqpr",
    phonenumber=" 0639741322",
    country="Italy",
    state="RM",
    city="Roma",
    lat=41.89,
    lon=12.49,
)

health_authority_not_written = dict(
    email="campobasso@asl.it",
    name="ASL Campobassso",
    password="romamolesta",
    phonenumber=" 0874777777",
    country="Italy",
    state="CB",
    city="Campobaso",
    lat=39.89,
    lon=14.49,
)

mark = dict(
    user_id=1,
    authority_id=1,
    duration=14,
)

restaurant1 = dict(
    name="Trattoria da Gino",
    lat=64.36,
    lon=85.24,
    phone="+39 561256145",
    time_of_stay=180,
    cuisine_type="ETHNIC",
    opening_hours=10,
    closing_hours=24,
    operator_id=1,
    average_rating=3.7,
    precautions=["Amuchina", "Social distancing"],
)

table1 = {"name": "A4", "seats": 4, "restaurant_id": 1}

table2 = {"name": "B10", "seats": 10, "restaurant_id": 1}

table3 = {"name": "C10", "seats": 10, "restaurant_id": 1}

table4 = {"name": "D10", "seats": 10, "restaurant_id": 1}

table5 = {"name": "E10", "seats": 10, "restaurant_id": 1}

table6 = {"name": "F10", "seats": 10, "restaurant_id": 1}

booking1 = {
    "user_id": 1,
    "restaurant_id": 1,
    "start_booking": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "end_booking": (datetime.now() + timedelta(hours=2, minutes=30)).strftime(
        "%Y-%m-%d %H:%M"
    ),
    "confirmed_booking": True,
    "seats": 1,
}

booking2 = {
    "user_id": 2,
    "restaurant_id": 1,
    "start_booking": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "end_booking": (datetime.now() + timedelta(hours=2, minutes=30)).strftime(
        "%Y-%m-%d %H:%M"
    ),
    "confirmed_booking": False,
    "seats": 2,
}

booking2_confirm = {
    "booking_number": 2,
    "users": [
        {
            "firstname": "Linus",
            "lastname": "Torvalds",
            "email": "linus@torvalds.com",
            "fiscalcode": "FCGZPX89A57E015V",
        }
    ],
}

booking3 = {
    "user_id": 3,
    "restaurant_id": 1,
    "start_booking": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "end_booking": (datetime.now() + timedelta(hours=2, minutes=30)).strftime(
        "%Y-%m-%d %H:%M"
    ),
    "confirmed_booking": True,
    "seats": 1,
}

booking4 = {
    "user_id": 4,
    "restaurant_id": 1,
    "start_booking": (datetime.now() + timedelta(hours=2, minutes=30)).strftime(
        "%Y-%m-%d %H:%M"
    ),
    "end_booking": (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
    "start_booking": "2020-11-05 12:00",
    "end_booking": "2020-11-05 14:30",
    "confirmed_booking": True,
    "seats": 1,
}

booking5 = {
    "user_id": 5,
    "restaurant_id": 1,
    "start_booking": (datetime.now() - timedelta(hours=2, minutes=30)).strftime(
        "%Y-%m-%d %H:%M"
    ),
    "end_booking": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "confirmed_booking": True,
    "seats": 1,
}

checkin1 = {"booking_number": 1, "user_list": [{"user_id": 1}]}

checkin2 = {"booking_number": 2, "user_list": [{"user_id": 2}, {"user_id": 6}]}

checkin4 = {"booking_number": 4, "user_list": [{"user_id": 4}]}

checkin5 = {"booking_number": 5, "user_list": [{"user_id": 5}]}
