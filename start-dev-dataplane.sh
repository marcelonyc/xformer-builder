#! /bin/bash

export PYTHONPATH=$PYTHONPATH:./lib

while [ true ]
do 
    fastapi dev dataplane/src/app.py
done
