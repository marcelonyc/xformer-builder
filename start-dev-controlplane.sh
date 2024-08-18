#! /bin/bash

export PYTHONPATH=$PYTHONPATH:./lib
CONFIG_FILE=$1
python controlplane/src/dash_app.py $CONFIG_FILE
