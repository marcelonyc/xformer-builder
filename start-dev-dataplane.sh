#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../../
GUNICORN_CONFIG_FILE="$(pwd)/dataplane/gunicorn/gunicorn_conf.py"
  
# If you want to enable dash or app debug mode run this exports 
# in the terminal cbefore running the script
# export DASH_DEBUG=True
# export LOG_LEVEL=info



CONFIG_FILE=$1
cd dataplane/src

export PYTHONPATH=$PYTHONPATH:../../
export RUN_MODE=dev

alembic upgrade head

gunicorn --forwarded-allow-ips "*" --workers 1 -c ${GUNICORN_CONFIG_FILE} app:app
# fastapi dev --port 9000 app.py

