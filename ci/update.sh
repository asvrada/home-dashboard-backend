#!/usr/bin/env bash
# This script will pull the latest GitHub commit and run build

echo "Running update.sh"

if [[ -z $ROOT_HOME_DASHBOARD_BACKEND ]]; then
    echo "ROOT_HOME_DASHBOARD_BACKEND is empty"
    exit 1
fi

cd $ROOT_HOME_DASHBOARD_BACKEND
git pull --ff-only

docker-compose stop
docker-compose up -d --build

echo "Finished update.sh"
