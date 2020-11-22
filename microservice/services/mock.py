from faker import Faker
from codicefiscale import codicefiscale as cf
import datetime

from microservice import db
from microservice.models import (
    User,
    Operator,
    HealthAuthority,
    Mark,
)

fake = Faker("it_IT")


def everything():
    users(10)
    operators()
    health_authority()
    mark_three_users()


def users(n=50):
    """
    Add a random number of users in the database, together with the default user.
    This method is not stable yet. Avoid using big numbers.

    Args:
        n (int, optional): Number of user to generate. Defaults to 50.
    """
    users_number = db.session.query(User).count()
    if users_number == 0:
        default_user()

        users = list()
        for i in range(0, n - 1):
            profile = fake.profile(["mail", "birthdate", "sex"])
            profile["first_name"] = fake.first_name()
            profile["last_name"] = fake.last_name()

            # Generate fiscal code
            fiscal_code = None
            while fiscal_code is None:
                try:
                    fiscal_code = cf.encode(
                        name=profile["first_name"],
                        surname=profile["last_name"],
                        sex=profile["sex"],
                        birthdate=profile["birthdate"].strftime("%d/%m/%Y"),
                        birthplace=fake.city(),
                    )
                except ValueError:
                    pass

            users.append(
                User(
                    email=profile["mail"],
                    firstname=profile["first_name"],
                    lastname=profile["last_name"],
                    phonenumber=fake.phone_number().replace(" ", ""),
                    password=fake.password(length=fake.pyint(8, 24)),
                    birthdate=profile["birthdate"],
                    fiscalcode=fiscal_code,
                )
            )

        db.session.add_all(users)
        db.session.commit()


def default_user():
    q = db.session.query(User).filter(User.email == "example@example.com")
    user = q.first()
    if user is None:
        example = User(
            email="example@example.com",
            firstname="Admin",
            lastname="Admin",
            password="admin",
            phonenumber=3330049382,
            birthdate=datetime.datetime(2020, 10, 5),
        )
        db.session.add(example)
        example = User(
            email="gino@pasticcino.com",
            firstname="Admin",
            lastname="Admin",
            password="admin",
            phonenumber=3330049381,
            birthdate=datetime.datetime(2020, 10, 5),
        )
        db.session.add(example)
        db.session.commit()


def operators(n=50):
    """
    Add a random number of operators in the database, together with the default operators.
    This method is not stable yet. Avoid using big numbers.

    Args:
        n (int, optional): Number of operators to generate. Defaults to 50.
    """
    operators_number = db.session.query(Operator).count()
    if operators_number == 0:
        default_operator()

        operators = list()
        for i in range(0, n - 1):
            profile = fake.profile(["mail", "birthdate", "sex"])
            profile["first_name"] = fake.first_name()
            profile["last_name"] = fake.last_name()

            # Generate fiscal code
            fiscal_code = None
            while fiscal_code is None:
                try:
                    fiscal_code = cf.encode(
                        name=profile["first_name"],
                        surname=profile["last_name"],
                        sex=profile["sex"],
                        birthdate=profile["birthdate"].strftime("%d/%m/%Y"),
                        birthplace=fake.city(),
                    )
                except ValueError:
                    pass

            operators.append(
                Operator(
                    email=profile["mail"],
                    firstname=profile["first_name"],
                    lastname=profile["last_name"],
                    phonenumber=fake.phone_number().replace(" ", ""),
                    password=fake.password(length=fake.pyint(8, 24)),
                    birthdate=profile["birthdate"],
                    fiscalcode=fiscal_code,
                )
            )

        db.session.add_all(operators)
        db.session.commit()


def default_operator():
    q = db.session.query(Operator).filter(Operator.email == "operator@example.com")
    user = q.first()
    if user is None:
        example = Operator()
        example.firstname = "OperatorAdmin"
        example.lastname = "OperatorAdmin"
        example.email = "operator@example.com"
        example.birthdate = datetime.datetime(2020, 10, 9)
        example.is_admin = True
        example.password = "admin"
        example.fiscalcode = "my_fiscal_code"
        db.session.add(example)

        example = Operator()
        example.firstname = "OperatorAdmin"
        example.lastname = "OperatorAdmin"
        example.email = "operator1@example.com"
        example.birthdate = datetime.datetime(2020, 10, 9)
        example.is_admin = True
        example.password = "admin"
        example.fiscalcode = "my_fiscal_code"
        db.session.add(example)
        db.session.commit()


def health_authority():
    ha = (
        db.session.query(HealthAuthority)
        .filter(HealthAuthority.email == "auth@mail.com")
        .first()
    )
    if ha is None:
        example = HealthAuthority()
        example.name = "Admin"
        example.email = "auth@mail.com"
        example.password = "admin"
        example.phone = 3330049383
        example.country = "Italy"
        db.session.add(example)
        db.session.commit()


def mark_three_users():
    if not Mark.query.all():
        user1 = db.session.query(User).filter(User.id == 4).first()
        user2 = db.session.query(User).filter(User.id == 7).first()
        user3 = db.session.query(User).filter(User.id == 8).first()

        ha = db.session.query(HealthAuthority).filter(HealthAuthority.id == 1).first()
        ha.mark(user1)
        ha.mark(user2)
        ha.mark(user3)

        db.session.commit()
