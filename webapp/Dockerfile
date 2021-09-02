#########
### Node image for building static assets
######
FROM node:16-alpine as node_builder
ENV NODE_ENV=production

WORKDIR /app

COPY ./client/package.json ./client/yarn.lock ./client/
RUN cd ./client && yarn install --production

COPY ./client ./client
RUN cd ./client && yarn build

#########
### Python image for running webapp and cron jobs
######
FROM python:3.9.7-slim-buster AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Required by prometheus-flask-exporter
ENV prometheus_multiproc_dir '/tmp'

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends --yes curl cron procps && rm -rf /var/lib/apt/lists/\*
# Set up log forwarding to docker log collector (used by cron jobs)
# cf: https://docs.docker.com/config/containers/logging/ (mixing nginx & httpd approach)
RUN ln -sf /proc/1/fd/1 /app/cronjob_output

COPY ./entrypoint.sh /entrypoint.sh

RUN pip install --upgrade pip pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install

COPY ./cron.d/* /etc/cron.d/

COPY . .
RUN ./scripts/babel_run.sh

EXPOSE 5000

ENTRYPOINT [ "/entrypoint.sh" ]

#########
### cron target
######
FROM base AS cron
CMD ["/usr/sbin/cron", "-f"]

#########
### webapp target
######
FROM base AS webapp

COPY --from=node_builder /app/app/static /app/app/static
# Need to set these env variables for flask-static-digest to be able to run. The fact that we're using 'development'
# makes no difference to how it runs, it's just the easiest.
RUN FLASK_ENV=development pipenv run flask digest compile

CMD [ "gunicorn", "--config", "gunicorn_config.py", "autoapp:app" ]
