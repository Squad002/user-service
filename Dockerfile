FROM python:3.8.5-slim-buster

# Environment variables for the configuration
ENV FLASK_APP app.py
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create non-root user and home folder
RUN useradd -m gooutsafe
WORKDIR /home/gooutsafe

# Install dependencies
COPY requirements/ requirements/
RUN python -m venv venv
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
