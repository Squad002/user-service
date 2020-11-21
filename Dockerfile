FROM python:3.8.5-alpine

# Environment variables for the configuration
ENV FLASK_APP app.py
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create non-root user and home folder
RUN adduser -D gooutsafe
WORKDIR /home/gooutsafe

# Install dependencies
COPY requirements/ requirements/
RUN python -m venv venv
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev && \
    venv/bin/pip install --no-cache-dir cryptography==3.2.1 && \
    apk del gcc musl-dev libffi-dev openssl-dev python3-dev
RUN venv/bin/pip install -r requirements/docker.txt 

# Move code
COPY microservice/ microservice/
COPY app.py config.py boot.sh openapi.yml ./

# Permissions
RUN chown -R gooutsafe:gooutsafe ./
RUN chmod a+x boot.sh

EXPOSE 5000
USER gooutsafe
ENTRYPOINT [ "./boot.sh" ]
