# from microservice import db
# from microservice.models import User
from connexion import request


def bucchino():
    request.get_data()
    user = request.json
    print(user)

    x = User(firstname="asjlkfasdfj")
    db.session.add(x)
    db.session.commit()

    # new_user = db.session.query(User.id).filter_by(email=user["email"]).first()
    if new_user:
        return 409
    else:
        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password=user.password,
            birthdate=user.birthdate,
            phone_number=user.phonenumber,
            fiscal_code=user.fiscal_code,
        )

        db.session.add(new_user)
        db.session.commit()

        return 201


def get():
    pass


def pippo():
    pass


def patch():
    pass


def delete():
    pass
