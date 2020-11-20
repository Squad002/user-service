import logging

import connexion
from flask_sqlalchemy import SQLAlchemy

from connexion.resolver import RestyResolver


logging.basicConfig(level=logging.INFO)
connexion_app = connexion.App(__name__, specification_dir="../")

db = SQLAlchemy()


def create_app():
    # Get the underlying Flask app instance
    flask_app = connexion_app.app
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from microservice.models.user import User

db.create_all(app=flask_app)


connexion_app.add_api("openapi.yml")  # , resolver=RestyResolver("microservice.api"))


new_user = db.session.query(User.id).filter_by(email="mammt").first()
print(new_user)

if __name__ == "__main__":
    # run our standalone gevent server
    connexion_app.run(port=8080)
