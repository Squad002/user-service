from microservice import create_app

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app, connexion_app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.logger.info("Botting finished")

# if __name__ == "__main__":
#     connexion_app.run(port=8080)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    pass