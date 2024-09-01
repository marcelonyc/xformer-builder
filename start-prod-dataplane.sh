#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../../
GUNICORN_CONFIG_FILE="$(pwd)/dataplane/gunicorn/gunicorn_conf.py"


export APP_CONFIG_FILE=$1
cd dataplane/src

export RUN_MODE=prod

alembic upgrade head

gunicorn --forwarded-allow-ips "*"  -c ${GUNICORN_CONFIG_FILE} app:app



