from datetime import datetime
from microservice import db
from microservice.models import AbstractUser, Operator, Mark

import logging

logger = logging.getLogger("monolith")


class HealthAuthority(AbstractUser):
    __tablename__ = "authority"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128))
    name = db.Column(db.Unicode(128))
    password_hash = db.Column(db.Unicode(128))
    phonenumber = db.Column(db.Unicode(40))

    country = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(128))
    city = db.Column(db.Unicode(128))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    marks = db.relationship("Mark", back_populates="authority")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def mark(self, user: Operator, duration=14, starting_date=datetime.utcnow()):
        logger.info(
            f"Authority (id={self.id}, name={self.name}) just marked the user (ID={user.id}, firstname={user.firstname})"
        )
        self.marks.append(
            Mark(user=user, authority=self, duration=duration, created=starting_date)
        )

    def serialize(self, keys):
        return dict([(k, v) for k, v in self.__dict__.items() if k in keys])
