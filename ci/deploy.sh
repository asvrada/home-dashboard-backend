#!/usr/bin/env bash

echo "Running deploy.sh"

# Call Servicebus
SERVICEBUS_ENDPOINT="https://jeff-servicebusclient.azurewebsites.net"

curl -d '{"repo":"home-dashboard-backend"}' -H 'Content-Type: application/json' -X POST $SERVICEBUS_ENDPOINT

echo "Finished deploy.sh"
