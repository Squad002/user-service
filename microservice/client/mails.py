from flask import current_app
from microservice.client.breakers import read_request_breaker

import requests


@read_request_breaker
def send_email(title, body, recipients):
    res = requests.post(
        f"{current_app.config['URL_API_BOOKING']}mails/{id}",
        json={
            "sender": "gooutsafe-no-reply@mail.com",
            "html_body": body,
            "recipients": recipients,
            "subject": title,
            "text_body": body,
        },
        timeout=(
            current_app.config["READ_TIMEOUT"],
            current_app.config["WRITE_TIMEOUT"],
        ),
    )

    return res.json()
