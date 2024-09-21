
forge verify-contract --etherscan-api-key $ETHERSCAN_API_KEY 0x0897B75a68b6536E961C81300315918227cC18BA src/ERC20Swap.sol:ERC20Swap --chain 11155111 --watch \
--constructor-args $( cast abi-encode "constructor(uint256,uint256)" 10800 86400 )
