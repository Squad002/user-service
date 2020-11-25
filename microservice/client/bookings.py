from flask import current_app
from microservice.client.breakers import read_request_breaker

import requests


@read_request_breaker
def get_bookings_by_user_id(user_id):
    res = requests.get(
        f"{current_app.config['URL_API_BOOKING']}bookings?user_id={user_id}",
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    return res.json()


@read_request_breaker
def get_bookings_by_restaurant_id(restaurant_id):
    res = requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings?restaurant_id={restaurant_id}",
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    return res.json()


@read_request_breaker
def get_bookings_by_table_id(table_id):
    res = requests.post(
        f"{current_app.config['URL_API_BOOKING']}bookings?table_id={table_id}",
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    return res.json()