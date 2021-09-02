#!/bin/sh
set -e

# Set environment variables for cron job (loaded automatically by python-dotenv)
rm -f /app/.env
touch /app/.env
set +x  # Turn off command logging to avoid leaking secrets
echo "PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE" >> /app/.env
echo "PYTHONUNBUFFERED=$PYTHONUNBUFFERED" >> /app/.env
echo "FLASK_ENV=$FLASK_ENV" >> /app/.env
echo "FLASK_APP=autoapp" >> /app/.env
echo "ERICA_BASE_URL=$ERICA_BASE_URL" >> /app/.env
echo "RATELIMIT_STORAGE_URL=$RATELIMIT_STORAGE_URL" >> /app/.env
echo "SQLALCHEMY_DATABASE_URI=$SQLALCHEMY_DATABASE_URI" >> /app/.env
echo "RSA_ENCRYPT_PUBLIC_KEY=$RSA_ENCRYPT_PUBLIC_KEY" >> /app/.env
echo "IDNR_SALT=$IDNR_SALT" >> /app/.env
echo "prometheus_multiproc_dir=$prometheus_multiproc_dir" >> /app/.env
set -x  # Turn command logging back on

# Hand off to the CMD
exec pipenv run "$@"
