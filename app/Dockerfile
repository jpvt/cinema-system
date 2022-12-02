# Use the official image as a parent image.
FROM python:3.7-slim-buster

# Set the working directory.
COPY . /app
WORKDIR /app

# Run the command inside your image filesystem.
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && pip install cryptography \
    && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
RUN pip install -r requirements.txt
RUN pip install nose

RUN chmod +x run.sh

ENV HASURA_HOST="http://localhost/v1/graphql"
ENV HASURA_PREFIX="app_"

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8501

# Run the specified command within the container.
CMD [ "./run.sh" ]