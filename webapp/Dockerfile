FROM python:3.9.5-slim-buster AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

# Required by prometheus-flask-exporter
ENV prometheus_multiproc_dir '/tmp'

FROM base AS cron
CMD ["/usr/sbin/cron", "-f"]

FROM base AS webapp
CMD [ "gunicorn", "--config", "gunicorn_config.py", "app:app" ]

