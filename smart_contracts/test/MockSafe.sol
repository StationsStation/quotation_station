// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

// ERC-20 interface 
interface IERC20Swap {
    function claimRelay(uint256 swapId, bytes32 secret, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external;
    function newSwap(
        address buyer,
        bytes32 secretHash,
        uint256 expiration,
        address token,
        uint256 amount,
        bool swapSide
    ) external payable returns (uint256 swapsId);
}

// ERC-20 interface for interacting with the USDC token
interface IERC20 {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
    function decimals() external view returns (uint8);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

// Not compatible with 1.3 Safe, just Mock with isValidSignature(bytes32 hash, bytes memory signature)
contract MockSafe {
    bytes4 constant internal MAGICVALUE = 0x1626ba7e;
    mapping (bytes32 => bytes32) public mapSig;

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

    function setSig(bytes32 hash, uint8 v, bytes32 r, bytes32 s) external returns (bytes memory) {
        bytes memory sig = concatSignature(v, r, s);
        mapSig[hash] = keccak256(abi.encode(sig));
        return sig;
    }

    function isValidSignature(bytes32 hash, bytes memory sig) external view returns (bytes4) {
        if(mapSig[hash] == keccak256(abi.encode(sig))) {
            return MAGICVALUE;
        } else {
            return 0;
        }
    }

    function claimRelay(address swap, uint256 swapId, bytes32 secret, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external {
        IERC20Swap(swap).claimRelay(swapId, secret, deadline, v, r, s);
    }

    // ERC20 token only 
    function newSwap(
        address swap,
        address buyer,
        bytes32 secretHash,
        uint256 expiration,
        address token,
        uint256 amount,
        bool swapSide
    ) external payable returns (uint256 swapsId) {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        IERC20(token).approve(swap, amount);
        swapsId = IERC20Swap(swap).newSwap(
            buyer,
            secretHash,
            expiration,
            token,
            amount,
            swapSide
        ); 
    }

}