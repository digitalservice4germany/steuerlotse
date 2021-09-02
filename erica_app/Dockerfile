FROM python:3.9.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG bucket_name
ARG access_key_id
ARG access_key
ARG endpoint_url
ARG elster_datenlieferant
ARG elster_hersteller_id
ENV ELSTER_DATENLIEFERANT=$elster_datenlieferant
ENV ELSTER_HERSTELLER_ID=$elster_hersteller_id

WORKDIR /app

RUN apt-get update && apt-get install -y pcsc-tools pcscd procps unzip && rm -rf /var/lib/apt/lists/\*

# Install debugging tools
# RUN apt-get update && \
#  apt-get install -y vim telnet coreutils less strace lsof rsyslog usbutils && \
#  rm -rf /var/lib/apt/lists/\*

RUN pip install --upgrade pip pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install

COPY ./entrypoint.sh /entrypoint.sh

COPY . .
RUN env ERICA_BUCKET_NAME=$bucket_name AWS_ACCESS_KEY_ID=$access_key_id AWS_SECRET_ACCESS_KEY=$access_key ENDPOINT_URL=$endpoint_url pipenv run python scripts/load_eric_binaries.py download-eric-cert-and-binaries

EXPOSE 8000

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "python", "-m", "erica" ]
