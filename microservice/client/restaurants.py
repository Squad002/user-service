from flask import current_app
from microservice.client.breakers import read_request_breaker

import requests


@read_request_breaker
def get_restaurant_by_id(id):
    res = requests.get(
        f"{current_app.config['URL_API_RESTAURANT']}restaurants/{id}",
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    return res.json() if res.json() else None


@read_request_breaker
def get_tables_by_restaurant_id(id):
    res = requests.get(
        f"{current_app.config['URL_API_RESTAURANT']}tables?restaurant_id={id}",
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    return res.json()