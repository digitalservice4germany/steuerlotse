FROM python:3.9.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ERICA_BUCKET_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG ENDPOINT_URL
ARG ELSTER_DATENLIEFERANT
ARG ELSTER_HERSTELLER_ID
ENV ERICA_BUCKET_NAME=$ERICA_BUCKET_NAME
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV ENDPOINT_URL=$ENDPOINT_URL
ENV ELSTER_DATENLIEFERANT=$ELSTER_DATENLIEFERANT
ENV ELSTER_HERSTELLER_ID=$ELSTER_HERSTELLER_ID

WORKDIR /app

RUN apt-get update && apt-get install -y pcsc-tools pcscd procps unzip && rm -rf /var/lib/apt/lists/\*


RUN pip install --upgrade pip pipenv boto3
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system

COPY . .

# Get tax office list and ERiC libraries
RUN python scripts/load_eric_binaries.py download-eric-cert-and-binaries
RUN env ERICA_ENV=testing python scripts/create_tax_office_lists.py create
EXPOSE 8000

#ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "python", "-m", "erica" ]
