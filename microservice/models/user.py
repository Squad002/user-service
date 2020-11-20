from microservice import db
from microservice.models import AbstractUser
from datetime import datetime, timedelta


class User(AbstractUser):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avatar_id = db.Column(db.Unicode(128))

    firstname = db.Column(db.Unicode(128), nullable=False)
    lastname = db.Column(db.Unicode(128))
    password_hash = db.Column(db.Unicode(128))
    fiscal_code = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    phone_number = db.Column(db.Unicode(40))
    birthdate = db.Column(db.DateTime)

    marks = db.relationship("Mark", back_populates="user")
    # booking = db.relationship("Booking", back_populates="user")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        from hashlib import sha1
        from base64 import b32encode

        hashed = sha1((datetime.utcnow().isoformat() + self.firstname).encode("utf-8"))
        self.avatar_id = b32encode(hashed.digest()).decode("utf-8")

    def has_been_marked(self) -> bool:
        """Returns weather the user has been marked in the past or is currently marked.

        Returns:
            bool: boolean value
        """
        if self.marks:
            return True
        else:
            False

    def is_marked(self) -> bool:
        """Returns weather the user is currently marked.

        Returns:
            bool: boolean value
        """
        return self.has_been_marked() and self.get_remaining_mark_days() > 0

    def get_last_mark(self):
        """
        Returns the last mark that has been done.
        The supposition, is that the last one made, is more accurate.
        Thus if the previous one lasts longer than the new one, the new one is still accepted.

        Returns:
            Mark: the last one that has been done.
        """
        return max(self.marks, key=lambda mark: mark.created)

    def get_last_mark_duration(self):
        return self.get_last_mark().duration

    def get_mark_expiration_date(self, from_date=datetime.utcnow()) -> datetime:
        last_mark = self.get_last_mark()
        return last_mark.created + timedelta(days=last_mark.duration + 1)

    def get_remaining_mark_days(self, from_date=datetime.utcnow()):
        return (self.get_mark_expiration_date() - from_date).days - 1

    def has_been_deleted(self) -> bool:
        """Returns weather the user has unsubscribed

        Returns:
            bool: boolean value
        """
        return self.email == "deleted@deleted.it"

    # def get_bookings(self, from_date=datetime.utcnow(), range_duration=14):
    #     """
    #         It returns a list of bookings that the user made in a range from a starting date.
    #     Args:
    #         from_date (datetime, optional): is the date from which to start searching. Defaults to datetime.utcnow().
    #         range_duration (int, optional): it's the range of days. Defaults to 14.

    #     Returns:
    #         [type]: [description]
    #     """
    #     return [
    #         b
    #         for b in self.booking
    #         if b.start_booking >= (from_date - timedelta(days=range_duration))
    #     ]

    # def check_equality_for_booking(self, firstname, lastname, email):
    #     return (
    #         self.firstname == firstname
    #         and self.lastname == lastname
    #         and self.email == email
    #     )

    def get_avatar_link(self):
        from flask import current_app

        return current_app.config["AVATAR_PROVIDER"].format(seed=self.avatar_id)

    def serialize(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != "_"])
