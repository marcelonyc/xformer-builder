#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../../
GUNICORN_CONFIG_FILE="$(pwd)/controlplane/gunicorn/gunicorn_conf.py"
  
# If you want to enable dash or app debug mode run this exports 
# in the terminal cbefore running the script
# export DASH_DEBUG=True
# export LOG_LEVEL=info



CONFIG_FILE=$1
cd controlplane/src

gunicorn -k gevent --forwarded-allow-ips "*" -c ${GUNICORN_CONFIG_FILE} dash_app:server
# python dash_app.py