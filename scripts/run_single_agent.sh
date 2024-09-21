#!/usr/bin/env bash

set -e 

REPO_DIR=$(git rev-parse --show-toplevel)

agent_author=$(echo $1 | cut -d'/' -f1)
agent_name=$(echo $1 | cut -d'/' -f2)

# remove if already existing
if [ -d "$agent_name" ]; then
    rm -r "$agent_name"
fi

# fetch the agent from the local package registry
echo "Fetching agent $1 from the local package registry..."
aea -s fetch $1 --local > /dev/null

cd $agent_name

# create and add a new ethereum key
if [ ! -f ../ethereum_private_key.txt ]; then
    aea -s generate-key ethereum && aea -s add-key ethereum
else
    cp ../ethereum_private_key.txt ./ethereum_private_key.txt
    aea -s add-key ethereum 
fi
# install any agent deps
aea -s install

# issue certificates for agent peer-to-peer communications
if [ ! -f ../certs ]; then
    aea -s issue-certificates
else
    cp -r ../certs ./
fi

# spin up the Tendermint Flask server
CONFIG_FILE="$REPO_DIR/scripts/tendermint-docker-compose.yml"
docker compose -f $CONFIG_FILE up -d

# finally, run the agent
# We wait for 20 seconds or for the tm node to be ready.
tries=0
tm_started=false
while [ $tries -lt 20 ]; do
    tries=$((tries + 1))
    if curl localhost:8080/hard_reset > /dev/null 2>&1; then
        echo "Tendermint node is ready."
        tm_started=true
        break
    fi
    sleep 1
done
if [ "$tm_started" = false ]; then
    echo "Tendermint node did not start in time. Please verify that the docker tendermint node is running."
    exit 1
fi

echo "Starting the agent..."

aea -s run

echo "Killing tendermint"

docker compose -f $CONFIG_FILE kill && docker compose -f $CONFIG_FILE down
