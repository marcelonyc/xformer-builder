#! /bin/bash

export PYTHONPATH=$PYTHONPATH:./lib

while [ true ]
do 
    fastapi run dataplane/src/app.py
done
