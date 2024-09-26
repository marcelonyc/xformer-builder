#! /bin/bash

# This script is used by the docker container as the entrypoint
echo "Starting service: $SERVICE"
cd /app
if [ "$SERVICE" == "controlplane" ]; then
    echo "Starting controlplane service"
    ./start-prod-controlplane.sh $APP_CONFIG_FILE
elif [ "$SERVICE" == "dataplane" ]; then
    echo "Starting dataplane service"
    ./start-prod-dataplane.sh $APP_CONFIG_FILE
elif [ "$SERVICE" == "both" ]; then
    echo "Starting controlplane and dataplane services"
    ./start-prod-controlplane.sh $APP_CONFIG_FILE &
    ./start-prod-dataplane.sh $APP_CONFIG_FILE
else
    echo "Invalid service name"
    exit 1
fi