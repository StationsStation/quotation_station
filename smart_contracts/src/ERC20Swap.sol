// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import {SafeTransferLib} from "./SafeTransferLib.sol";

// TODO: comments
error AlreadyExists(uint256 swapId);
error NotExist(uint256 swapId);
error ZeroAddress();
error ZeroValue();
error Overflow(uint256 provided);

error IncorrectDurationMin(uint256 expected, uint256 provided);
error IncorrectDurationMax(uint256 expected, uint256 provided);
error BuyerOnly(address expected, address provided);
error SellerOnly(address expected, address provided);
error IncorrectHash(bytes32 secretHash, bytes32 secretHashCalc);
error Expiration(uint256 expected, uint256 provided);
error LowerThan(uint256 expected, uint256 provided);
error TransferFailed(address token, address from, address to, uint256 value);
error ReentrancyGuard();
error NonContract(address provided);

// ERC-20 interface 
interface IERC20 {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
    function decimals() external view returns (uint8);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

interface IERC1271 {
  /**
   * @dev Should return whether the signature provided is valid for the provided hash
   * @param _hash      Hash of the data to be signed
   * @param _signature Signature byte array associated with _hash
   */ 
  function isValidSignature(bytes32 _hash, bytes memory _signature) external view returns (bytes4);
}

contract ERC20Swap {
    event InitSwap(address indexed seller, address indexed buyer, bytes32 indexed secretHash, uint256 swapId, address token, uint256 amount, uint256 expirationClaim, uint256 expirationTotal, bool swapSide);
    event Claim(address indexed buyer, uint256 indexed swapId, bytes32 indexed secret, address token, uint256 amount, uint256 expiration);
    event Refund(address indexed seller, uint256 indexed swapId, address token, uint256 amount, uint256 expiration);

    enum Status {
        INVALID,
        PENDING,
        CLAIMED,
        REFUNDED
    } 

    struct Swap {
        address seller;
        address buyer;
        address token;
        uint96 amount;
        bytes32 secretHash;
        uint32 expirationClaim;
        uint32 expirationTotal;
        Status status;
        bytes32 secret;
    }
  
    uint32 public minTimelock;
    uint32 public maxTimelock;
    // Reentrancy lock
    uint256 internal _locked = 1;
    uint256 public nonce;
    string public constant VERSION = "1.2.0";
    address public constant ETH_TOKEN_ADDRESS = address(0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE);
    // bytes4(keccak256("isValidSignature(bytes32,bytes)")
    bytes4 constant internal MAGICVALUE = 0x1626ba7e;
    uint256 public constant MAGIC_M = 3;
    uint256 public constant MAGIC_N = 4; // m/n = 3/4 => duration * 3/4

    uint256 internal immutable INITIAL_CHAIN_ID;
    bytes32 internal immutable INITIAL_DOMAIN_SEPARATOR;

    mapping (uint256 => Swap) public swaps;

    // TODO: Natspecs
    constructor (uint256 _minTimelock, uint256 _maxTimelock) {
        minTimelock = uint32(_minTimelock); // 3 * 3600 or 3h
        maxTimelock = uint32(_maxTimelock); // 86400 or 24h
        INITIAL_CHAIN_ID = block.chainid;
        INITIAL_DOMAIN_SEPARATOR = computeDomainSeparator();
    }

    function newSwap(
        address buyer,
        bytes32 secretHash,
        uint256 expiration,
        address token,
        uint256 amount,
        bool swapSide
    ) external payable returns (uint256 swapsId)
    {
        // Reentrancy guard
        if (_locked > 1) {
            revert ReentrancyGuard();
        }
        _locked = 2;

        if(buyer == address(0) || token == address(0)) {
            revert ZeroAddress();
        }
        if(amount == 0) {
            revert ZeroValue();
        }
        if(amount > type(uint96).max) {
            revert Overflow(amount);
        }
        if(expiration > type(uint32).max) {
            revert Overflow(expiration);
        }

        // genue check if token is contract
        if(token.code.length > 0) {
            uint8 d = IERC20(token).decimals();
        } else {
            revert NonContract(token);
        }

        uint256 duration = expiration - block.timestamp;
        
        if(duration < minTimelock) {
            revert IncorrectDurationMin(minTimelock, duration);
        }
        
        if(duration > maxTimelock) {
            revert IncorrectDurationMax(maxTimelock, duration);
        }

        uint32 expirationClaim;
        uint32 expirationTotal;

        // swapSide == true if Alice swap
        // swapSide == false if Bob swap
        if(swapSide) {
            expirationClaim = uint32(expiration);
            expirationTotal = uint32(expiration);
        } else {
            expirationTotal = uint32(expiration);
            expirationClaim = uint32(block.timestamp + ((duration * MAGIC_M) / MAGIC_N)); 
        }

        // in case this is called in multisend mode
        uint256 localNonce = nonce;
        // Always unique
        swapsId = uint256(keccak256(abi.encode(
            block.chainid,
            buyer,
            msg.sender,
            expirationClaim,
            expirationTotal,
            token,
            amount,
            localNonce,
            blockhash(block.number - 1),
            block.timestamp
        )));

        nonce = localNonce++;

        swaps[swapsId] = Swap(
            msg.sender,
            buyer,
            token,
            uint96(amount),
            secretHash,
            expirationClaim,
            expirationTotal,
            Status.PENDING,
            0x0
        );

        emit InitSwap(
            msg.sender,
            buyer,
            secretHash,
            swapsId,
            token,
            amount,
            expirationClaim,
            expirationTotal,
            swapSide
        );

        if (token == ETH_TOKEN_ADDRESS) {
            if(msg.value < amount) {
                revert LowerThan(amount, msg.value);
            }
            if(msg.value > amount){
                uint256 change = msg.value - amount;
                (bool success, ) = msg.sender.call{value: change}("");
                if (!success) {
                    revert TransferFailed(ETH_TOKEN_ADDRESS, address(this), msg.sender, change);
                }
            }
        } else {
            SafeTransferLib.safeTransferFrom(token, msg.sender, address(this), amount);
        }
        _locked = 1;
    }

    function DOMAIN_SEPARATOR() public view returns (bytes32) {
        return block.chainid == INITIAL_CHAIN_ID ? INITIAL_DOMAIN_SEPARATOR : computeDomainSeparator();
    }

    function computeDomainSeparator() internal view virtual returns (bytes32) {
        return
            keccak256(
                abi.encode(
                    keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                    keccak256(bytes(VERSION)),
                    keccak256("1"),
                    block.chainid,
                    address(this)
                )
            );
    }

    function getMsgHash(address buyer, uint256 swapId, bytes32 secret, uint256 deadline) public view returns (bytes32) {
        return keccak256(
                    abi.encodePacked(
                        "\x19\x01",
                        DOMAIN_SEPARATOR(),
                        keccak256(
                            abi.encode(
                                keccak256(
                                    "claimRelay(address buyer, uint256 swapId, bytes32 secret, uint256 deadline)"
                                ),
                                buyer,
                                swapId,
                                secret,
                                deadline
                            )
                        )
                    )
                );
    }

    function concatSignature(uint8 v, bytes32 r, bytes32 s) internal pure returns (bytes memory sig){
        sig = new bytes(65);
        for (uint256 i; i < 32; i++) {
            sig[i] = r[i];
        }
		for (uint256 i=32; i < 64; i++) {
            sig[i] = s[i-32];
        }
		sig[64] = bytes1(v);
        return sig;
    }

    // ECDSA check and EIP-1271 check
    function _verifySig(address buyer, uint256 swapId, bytes32 secret, uint256 deadline, uint8 v, bytes32 r, bytes32 s) internal returns (bool){
        if(buyer.code.length > 0) {
            if(IERC1271(buyer).isValidSignature(getMsgHash(buyer, swapId, secret, deadline), concatSignature(v, r, s)) != MAGICVALUE) {
                return false;
            } 
        } else {
            // https://github.com/transmissions11/solmate/blob/e8f96f25d48fe702117ce76c79228ca4f20206cb/src/tokens/ERC20.sol
            // ledger issue
            if(v < 27) {
                v += 27;
            }
            address recoveredAddress = ecrecover(getMsgHash(buyer, swapId, secret, deadline), v, r, s);
            if(recoveredAddress == address(0)) {
                return false;
            }
            if(recoveredAddress != buyer) {
                return false;
            }
        }
        return true;
    }
    
    function claimRelay(uint256 swapId, bytes32 secret, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external {
        Swap storage swap = swaps[swapId];
        if(swap.status == Status.INVALID) {
            revert NotExist(swapId);
        }
        if(swap.status == Status.CLAIMED || swap.status == Status.REFUNDED) {
            revert ReentrancyGuard();
        }
        if(block.timestamp > swap.expirationClaim) {
            revert Expiration(swap.expirationClaim, block.timestamp);
        }
        if(block.timestamp > deadline) {
            revert Expiration(deadline, block.timestamp);
        }
        // eq: swap.buyer != "msg.sender"
        if(!_verifySig(swap.buyer, swapId, secret, deadline, v, r, s)) {
            revert BuyerOnly(swap.buyer, msg.sender);
        }
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        if(swap.secretHash != secretHash) {
            revert IncorrectHash(swap.secretHash, secretHash);
        } 
        swap.status = Status.CLAIMED;
        swap.secret = secret;
        emit Claim(msg.sender, swapId, secret, swap.token, swap.amount, swap.expirationClaim);

        if(swap.token == ETH_TOKEN_ADDRESS){
            (bool success, ) = msg.sender.call{value: swap.amount}("");
            if (!success) {
                revert TransferFailed(ETH_TOKEN_ADDRESS, address(this), msg.sender, swap.amount);
            }
        } else {
            SafeTransferLib.safeTransfer(swap.token, swap.buyer, swap.amount);
        }
    }

    function claim (uint256 swapId, bytes32 secret) external {
        Swap storage swap = swaps[swapId];
        if(swap.status == Status.INVALID) {
            revert NotExist(swapId);
        }
        if(swap.status == Status.CLAIMED || swap.status == Status.REFUNDED) {
            revert ReentrancyGuard();
        }
        if(swap.buyer != msg.sender) {
            revert BuyerOnly(swap.buyer, msg.sender);
        }
        if(block.timestamp > swap.expirationClaim) {
           revert Expiration(swap.expirationClaim, block.timestamp);
        }
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        if(swap.secretHash != secretHash) {
            revert IncorrectHash(swap.secretHash, secretHash);
        } 
        swap.status = Status.CLAIMED;
        swap.secret = secret;
        emit Claim(msg.sender, swapId, secret, swap.token, swap.amount, swap.expirationClaim);

        if(swap.token == ETH_TOKEN_ADDRESS){
            (bool success, ) = msg.sender.call{value: swap.amount}("");
            if (!success) {
                revert TransferFailed(ETH_TOKEN_ADDRESS, address(this), msg.sender, swap.amount);
            }
        } else {
            SafeTransferLib.safeTransfer(swap.token, swap.buyer, swap.amount);
        }
    }

    function refund (uint256 swapId) external {
        Swap storage swap = swaps[swapId];
        if(swap.status == Status.INVALID) {
            revert NotExist(swapId);
        }
        if(swap.status == Status.CLAIMED || swap.status == Status.REFUNDED) {
            revert ReentrancyGuard();
        }
        if(swap.seller != msg.sender) {
            revert SellerOnly(swap.seller, msg.sender);
        }
        if(block.timestamp < swap.expirationTotal) {
            revert Expiration(swap.expirationTotal, block.timestamp);
        }
        swap.status = Status.REFUNDED;
        emit Refund(msg.sender, swapId, swap.token, swap.amount, swap.expirationTotal);

        if(swap.token == ETH_TOKEN_ADDRESS){
            (bool success, ) = msg.sender.call{value: swap.amount}("");
            if (!success) {
                revert TransferFailed(ETH_TOKEN_ADDRESS, address(this), msg.sender, swap.amount);
            }
        } else {
            SafeTransferLib.safeTransfer(swap.token, swap.seller, swap.amount);
        }
    }
}