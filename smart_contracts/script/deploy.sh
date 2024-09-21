#!/bin/bash
# https://book.getfoundry.sh/forge/deploying
source .env

forge create --rpc-url $RPCURL_SEPOLIA \
    --constructor-args  10800 86400 \
    --private-key $PK \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify src/ERC20Swap.sol:ERC20Swap
