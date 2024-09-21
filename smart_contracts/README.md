# Atomic swap (EVM ERC20)
## Theory
References:
https://en.bitcoin.it/wiki/Atomic_swap <br>
https://github.com/bitcoin/bips/blob/master/bip-0199.mediawiki <br>
https://github.com/ethereum/EIPs/issues/1631 <br>
https://scryptplatform.medium.com/cross-chain-atomic-swaps-f13e874fcaa7 <br>
https://ethglobal.com/showcase/bch-evm-cross-chain-swap-ap4wj <br>
https://github.com/AthanorLabs/atomic-swap/blob/master/docs/protocol.md <br>


## Crypto protocol (EVM). Version 1.2.0
1. Alice in chain a, Alice has an address `alice_address` (EOA/Smart contract) controlled amount_a tokens ERC20 TokenA
2. Bob in chain b, Bob has an address `bob_address` (EOA/Smart contract) controlled amount_b tokens ERC20 TokenB 
3. Alice (or whoever else, it doesn't matter for the protocol) deployed ERC20Swap.sol in chain a
4. Bob (or whoever else, it doesn't matter for the protocol) deployed ERC20Swap.sol in chain b
5. Alice generates a secure random number `x` (256bit) and computes its hash: `h` = `SHA256(x)`
6. Alice call ERC20Swap.newSwap() with `expiration`,`secretHash` = `h`,`buyer` = `bob_address` in chain `a`, `seller` = `alice_address` in chain `a`, TokenA with amount_a, `swapSide` = `true`.
6.1. Alice transfered amount_a to `ERC20Swap` during `newSwap()` <br>
6.2. Alice emitted event with all params, including swap_id  <br>
7. Bob monitors events in the contract and sees that he is satisfied with the proposed conditions. if `swapSide` on Alice not `true`, Bob or doesn't accept the deal (by default). 
OR <br>
Alice sends him a message that such a swap has been created via off-chain. <br>
8. Bob call ERC20Swap.newSwap() with `expiration`,`secretHash` = `h`,`buyer` = `alice_address` in chain `b`, `seller` = `bob_address` in chain `b`, TokenB with amount_b, `swapSide` = false.
8.1. Bob transferred amount_b to `ERC20Swap` during `newSwap()` <br>
8.2. Bob emitted event with all params, including swap_id <br>
9. Alice monitors events in the contract and sees that she is satisfied with the proposed conditions. if `swapSide` on Bob not `false`, Alice or doesn't accept (ignore) the deal (by default). 
OR <br>
Bob sends him a message that such a swap has been created via off-chain. <br>
### happy path
10. Alice call `ERC20Swap.claim()` in chain `b` by providing `x`. TokenB amount_b will be transfered to Alice. Bob now knows `x` 
11. Bob call `ERC20Swap.claim()` in chain `a` by providing `x`. TokenA amount_a will be transferred to Bob.
12. Alice can't call `ERC20Swap.refund()` in chain `a`
13. Bob can't call `ERC20Swap.refund()` in chain `b`
14. Swap finished

### unhappy path
10. Alice wait to `expiration`, after call `ERC20Swap.refund()` in chain `a` and TokenA amount_a tranferred to Alice
11. Bob wait to `expiration`, after call `ERC20Swap.refund()` in chain `b` and TokenB amount_b tranferred to Bob

### happy path with relay
#### Source of idea based on `permit` ERC20.
10. Alice prepared (v,r,s) based on msgH(buyer, swapId, secret, deadline). Provider like Gelato (Dan) called `ERC20Swap.claimRelay()` (msg.sender is Dan, sign by Alice) in chain `b` by providing `x`. TokenB amount_b will be transfered to Alice. Bob now knows `x`
11. Bob prepared (v,r,s) based on msgH(buyer, swapId, secret, deadline).  Provider like Gelato (Dan) called `ERC20Swap.claimRelay()` (msg.sender is Dan, sign by Bob) in chain `a` by providing `x`. TokenA amount_a will be transferred to Bob.
Details Gelato SDK: https://docs.gelato.network/web3-services/relay/non-erc-2771/sponsoredcall <br>

### Key moment.
#### Moment 1
```
10. Alice call `ERC20Swap.claim()` in chain `b` by providing `x`. TokenB amount_b transferred to Alice. Bob now knows `x` 
After this, before the time expires, Bob must take back his.
If he does not do this, then Alice will take her tokens back. 
This is not a problem with the protocol itself, but a feature of it. 
```
#### Moment 2
```
If a revert occurs at the stage when sending tokens on claim, this is beyond the protocol.
Both parties trust the implementation of the tokens that are to be exchanged. 
If the other party does not trust the offered token, then it must refuse the exchange.
I advise to avoid `fee-on-transfer`, `rebasing`, and obviously scam-token
https://github.com/d-xo/weird-erc20 (example rebasing)
https://github.com/Defi-Cartel/salmonella (example scam)
Also, we cannot do anything in case `Tokens with Blocklists` (USDT) (Alice or Bob blacklisted in chain a or b)
```

## TODO
1. more timeout.
[x] fixed. v.1.1.0
2. unified status to enum Stage 
[x] fixed. v1.0.2
3. support native "token" like ETH, Matic, etc
[x] fixed, v.1.0.3
4. support Gelato gasless tx or another gasless solution (@8baller)
[x] fixed, v.1.2.0

## Build, test, deploy
### Forge install
```shell
curl -L https://foundry.paradigm.xyz | bash
# Set the environment variables as the tooltip says
foundryup
```
### ENV setup
```shell
cp env .env
vi .env
```
### Build
```shell
forge build
```
#### Run fork
```shell
# in separate shell window
source .env
anvil --fork-url $RPCURL --fork-block-number 20226778
or
anvil.sh
```
### Test
```shell
# fork testing
forge test --rpc-url http://127.0.0.1:8545/ --match-path test/ERC20Swap.t.sol -vv
```
### Deploy
```shell
source .env
forge create --rpc-url $RPCURL_SEPOLIA \
    --constructor-args  10800 86400 \
    --private-key $PK \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --verify src/ERC20Swap.sol:ERC20Swap
or
script/deploy.sh
```

## Addresses
### Sepolia
forge verify-contract --etherscan-api-key $ETHERSCAN_API_KEY 0x0897B75a68b6536E961C81300315918227cC18BA src/ERC20Swap.sol:ERC20Swap --chain 11155111 --watch \
--constructor-args $( cast abi-encode "constructor(uint256,uint256)" 10800 86400 )
++ cast abi-encode 'constructor(uint256,uint256)' 10800 86400
+ forge verify-contract --etherscan-api-key NX1KY4CYM4KDTU4TVEBJJ4RYC48SV89FNC 0x0897B75a68b6536E961C81300315918227cC18BA src/ERC20Swap.sol:ERC20Swap --chain 11155111 --watch --constructor-args 0x0000000000000000000000000000000000000000000000000000000000002a300000000000000000000000000000000000000000000000000000000000015180
Start verifying contract `0x0897B75a68b6536E961C81300315918227cC18BA` deployed on sepolia

Submitting verification for [src/ERC20Swap.sol:ERC20Swap] 0x0897B75a68b6536E961C81300315918227cC18BA.
Submitted contract for verification:
        Response: `OK`
        GUID: `fxpzvzypcnachgijvpiquxkf6twethqqzj2tm5thhui5b7mlu7`
        URL: https://sepolia.etherscan.io/address/0x0897b75a68b6536e961c81300315918227cc18ba
Contract verification status:
Response: `NOTOK`
Details: `Pending in queue`
Contract verification status:
Response: `OK`
Details: `Pass - Verified`
Contract successfully verified

v.1.2.0: 0x0897B75a68b6536E961C81300315918227cC18BA (verified) <br>


