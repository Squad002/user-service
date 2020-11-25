from microservice import db
from .abstract_user import AbstractUser


class Operator(AbstractUser):
    __tablename__ = "operator"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password_hash = db.Column(db.Unicode(128))
    fiscalcode = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128), nullable=False)
    phonenumber = db.Column(db.Unicode(40))
    birthdate = db.Column(db.Date)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def serialize(self, keys):
        return dict([(k, v) for k, v in self.__dict__.items() if k in keys])
