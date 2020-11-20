from microservice import db
from microservice.models.timestamp_mixin import TimestampMixin
from werkzeug.security import check_password_hash, generate_password_hash


class AbstractUser(TimestampMixin, db.Model):
    __abstract__ = True

    is_registered = db.Column(db.Boolean(), default=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        self.is_registered = True

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
