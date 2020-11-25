import os
from logging import FileHandler, Formatter

fileHandler = FileHandler("microservice.log", encoding="utf-8")
fileHandler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "top secret"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI") or "sqlite:///../gooutsafe.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # https://avatars.dicebear.com/api/avataaars/roma%20molesta.svg
    AVATAR_PROVIDER = "https://avatars.dicebear.com/api/avataaars/{seed}.svg"

    # Services
    URL_API_BOOKING = os.environ.get("URL_API_BOOKING") or "http://localhost:5002/"
    URL_API_RESTAURANT = (
        os.environ.get("URL_API_RESTAURANT") or "http://localhost:5003/"
    )
    URL_API_CELERY = os.environ.get("URL_API_CELERY") or "http://localhost:5004"
    READ_TIMEOUT = os.environ.get("READ_TIMEOUT") or 3.05
    WRITE_TIMEOUT = os.environ.get("WRITE_TIMEOUT") or 9.1

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    @staticmethod
    def init_app(app):
        app.logger.addHandler(fileHandler)


class DevelopmentConfig(Config):

    DEBUG = True

    @staticmethod
    def init_app(app):
        app.debug = True
        app.logger.addHandler(fileHandler)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///gooutsafe_test.db"
    )


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig,
}

mail_body_covid_19_mark = "Hey {},\nIn date {}, the health authority {} marked you positive to Covid-19. Contact your personal doctor to protect your health and that of others."
mail_body_covid_19_contact = "Hey {},\nIn date {}, while you were at restaurant {}, you could have been in contact with a Covid-19 case. Contact your personal doctor to protect your health and that of others."
mail_body_covid_19_operator_alert = "Hey {},\nIn date {}, at your restaurant {}, a Covid-19 case had a booking. Execute as soon as possible the health protocols."
mail_body_covid_19_operator_booking_alert = "Hey {},\nYou have a booking of a Covid-19 positive case, at your restaurant {}. The reservation ID is {} at table {}."