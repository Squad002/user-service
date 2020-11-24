from flask import request
from microservice import create_app, db
from microservice.services import mock
from microservice.models import User, Operator, HealthAuthority, Mark
from dotenv import load_dotenv

import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app, connexion_app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.logger.info("Booting finished")


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    mock.everything()


@app.route("/testing/services/user/db", methods=["GET", "DELETE"])
def delete_db():
    if request.method == "GET":
        return "Available", 204
    elif request.method == "DELETE":
        db.session.query(User).delete()
        db.session.query(Operator).delete()
        db.session.query(HealthAuthority).delete()
        db.session.query(Mark).delete()
        db.session.commit()

        return "OK", 204

    return "Error", 404
