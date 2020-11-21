[![Build Status](https://travis-ci.org/Squad002/user-service.svg?branch=main)](https://travis-ci.org/Squad002/user-service)
[![Coverage Status](https://coveralls.io/repos/github/Squad002/user-service/badge.svg?branch=main)](https://coveralls.io/github/Squad002/user-service?branch=main)

# GoOutSafe - User microservice

### Local
    # Install Dependencies
    pip install -r requirements/dev.txt

    # Deploy
    flask deploy

    # Run 
    export FLASK_APP="app.py"
    export FLASK_ENV=development
    flask run

### Docker Image
    docker build -t gooutsafe-user-service:latest . 
    docker run -p 5000:5000 gooutsafe-user-service 

## Tests with coverage
Inside user-service run (it will automatically use the configuration in pyproject.toml):

    pytest