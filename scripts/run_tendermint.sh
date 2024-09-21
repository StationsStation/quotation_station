#!/usr/bin/env bash

set -e 

# Check if Tendermint binary exists
if ! command -v tendermint &> /dev/null; then
    echo "Error: Tendermint binary not found. Make sure Tendermint is installed and added to the PATH."
    exit 1
fi

USER=$(whoami)
GROUP=$(id -gn)

# Set the home directory
export TMHOME=$HOME/tendermint_data/node1/

# Remove the existing Tendermint data directory if it exists
if [ -d "$TMHOME" ]; then
    echo "Removing existing Tendermint data directory..."
    rm -rf $TMHOME
fi

# Initialize configuration
tendermint init --home $TMHOME

# Set the environment variables
export PROXY_APP=tcp://localhost:26658

# Modify the configuration to create empty blocks
sed -i 's/create_empty_blocks = false/create_empty_blocks = true/' $TMHOME/config/config.toml

# Set ownership of the data directory
sudo chown -R $USER:$GROUP $TMHOME

# Start the node
tendermint node --proxy_app=$PROXY_APP --home $TMHOME
