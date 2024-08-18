#!/usr/bin/env sh

set -e

export PYTHONPATH=$PYTHONPATH:./lib


DATAPLANE_ROOT="./dataplane"

DEFAULT_MODULE_NAME=${DATAPLANE_ROOT}.src.app


MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

DEFAULT_GUNICORN_CONF=${DATAPLANE_ROOT}/gunicorn/gunicorn_conf.py
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"aiohttp.worker.GunicornWebWorker"}
LOG_LEVEL=${LOG_LEVEL:-debug}
LOG_CONFIG=${LOG_CONFIG:-${DATAPLANE_ROOT}/logging.ini}

# Check for DB updates 
cd $DATAPLANE_ROOT/src
alembic upgrade head
cd -


# Start Gunicorn
# gunicorn --forwarded-allow-ips "*" -k "$WORKER_CLASS" --log-config $LOG_CONFIG  -c "$GUNICORN_CONF" "$APP_MODULE"
gunicorn --forwarded-allow-ips "*" --log-config $LOG_CONFIG  -c "$GUNICORN_CONF" "$APP_MODULE"
