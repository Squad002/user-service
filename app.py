from microservice import create_app

import os

print("Going to create app")
app, connexion_app = create_app(os.getenv("FLASK_CONFIG") or "default")
print("App created")

if __name__ == "__main__":
    # run our standalone gevent server
    connexion_app.run(port=8080)
