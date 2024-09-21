// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import {Test, console} from "forge-std/Test.sol";
import {ERC20Swap} from "../src/ERC20Swap.sol";
import {MockSafe} from "./MockSafe.sol";

// ERC-20 interface for interacting with the USDC token
interface IERC20 {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
    function decimals() external view returns (uint8);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

// ERC-20 interface for interacting with the USDT token
interface IUSDT {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external;
    function decimals() external view returns (uint8);
    function approve(address spender, uint256 value) external;
    function transferFrom(address from, address to, uint256 value) external;
}


// TokenTransferTest is a contract that sets up and runs the test
contract ERC20SwapTest is Test {
    ERC20Swap public sw_alice;
    ERC20Swap public sw_bob;
    ERC20Swap public sw_dan;
    MockSafe  public dan_safe;

    IERC20 usdc;
    IERC20 uni;
    IERC20 olas;
    IUSDT usdt;

    address usdcAddress = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48; // USDC contract address on Ethereum Mainnet
    address usdtAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
    address uniAddress = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984;
    address olasAddress = 0x0001A500A6B18995B03f44bb040A5fFc28E45CB0;

    address whale = 0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf; // Polygon's ERC20 Bridge contract address on Ethereum Mainnet, used as a whale account
    address binance8 = 0xF977814e90dA44bFA03b6295A0616a897441aceC;
    address bitget = 0x1AB4973a48dc892Cd9971ECE8e01DcC7688f8F23;
    address moonpay = 0x0b5c4a7FcDA49e0a8661419Bb55B86161a86db2a;

    address alice;
    address bob;
    address dan;
    uint256 privateKeyDan = 0x1010101010101010101010101010101010101010101010101010101010101010;

    // setUp function runs before each test, setting up the environment
    function setUp() public {
        usdc = IERC20(usdcAddress); // Initialize the USDC contract interface
        uni = IERC20(uniAddress);
        olas = IERC20(olasAddress);
        usdt = IUSDT(usdtAddress);
        sw_alice = new ERC20Swap(0, 86400);
        sw_bob = new ERC20Swap(0, 86400);
        sw_dan = new ERC20Swap(0, 86400);
        dan_safe = new MockSafe();
        alice = vm.addr(1);
        bob = vm.addr(2);
        dan = vm.addr(privateKeyDan);
    }

    function testEOAasToken() public {
        address charlie = vm.addr(3);
        vm.startPrank(whale);
        uint256 depositAmountUSDC =  1000 * 10 ** usdc.decimals();
        usdc.transfer(alice, depositAmountUSDC);
        vm.stopPrank();
        
        bytes32 secret = bytes32(block.timestamp); // unsecure
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        uint256 expiration = block.timestamp + 3 * 60 * 60;

        vm.startPrank(alice); // Alice side
        usdc.approve(address(sw_alice), depositAmountUSDC);
        uint256 swAliceId1 = sw_alice.newSwap(bob, secretHash, expiration, usdcAddress, depositAmountUSDC / 2, true);
        vm.expectRevert();
        uint256 swAliceId2 = sw_alice.newSwap(bob, secretHash, expiration, charlie, depositAmountUSDC / 2, true);
        vm.stopPrank();
    }

    function testUSDTasToken() public {
        vm.startPrank(moonpay);
        uint256 depositAmountUSDT =  1000 * 10 ** usdt.decimals();
        usdt.transfer(alice, depositAmountUSDT);
        vm.stopPrank();
        
        bytes32 secret = bytes32(block.timestamp); // unsecure
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        uint256 expiration = block.timestamp + 3 * 60 * 60;

        vm.startPrank(alice); // Alice side
        usdt.approve(address(sw_alice), depositAmountUSDT);
        uint256 swAliceId = sw_alice.newSwap(bob, secretHash, expiration, usdtAddress, depositAmountUSDT, true);
        vm.stopPrank();
    }

    function testAliceBobSuccessSimpleNoTimeShift() public {
        // Impersonate the whale account for testing
        vm.startPrank(whale);
        //uint256 initialBalanceUSDC = usdc.balanceOf(whale); // Get the initial balance of whale
        //console.log("USDC initial balance: ", initialBalanceUSDC); // Log the final balance to the console
        uint256 transferAmountUSDC = 50000 * 10 ** usdc.decimals();
        uint256 depositAmountUSDC =  1000 * 10 ** usdc.decimals();
        usdc.transfer(bob, transferAmountUSDC);
        vm.stopPrank();

        vm.startPrank(bitget);
        //uint256 initialBalanceOLAS = olas.balanceOf(bitget); // Get the initial balance of whale
        //console.log("OLAS initial balance: ", initialBalanceOLAS); // Log the final balance to the console
        uint256 transferAmountOLAS = 50000 * 10 ** olas.decimals();
        uint256 depositAmountOLAS =  1000 * 10 ** olas.decimals();
        olas.transfer(alice, transferAmountOLAS);
        vm.stopPrank();

        bytes32 secret = bytes32(block.timestamp); // unsecure
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        uint256 expiration = block.timestamp + 3 * 60 * 60;

        vm.startPrank(alice); // Alice side
        olas.approve(address(sw_alice), depositAmountOLAS);
        uint256 swAliceId = sw_alice.newSwap(bob, secretHash, expiration, olasAddress, depositAmountOLAS, true);
        //console.log(swAliceId);
        vm.stopPrank();

        vm.startPrank(bob); // Bob side
        usdc.approve(address(sw_bob), depositAmountUSDC); 
        /// pseudo secretHash from events -->
        uint256 swBobId = sw_bob.newSwap(alice, secretHash, expiration, usdcAddress, depositAmountUSDC, false);
        //console.log(swBobId);
        vm.stopPrank();

        vm.startPrank(alice); // Alice side
        uint256 BalanceUSDCAlice = usdc.balanceOf(alice);         
        //console.log("Alice USDC balance before swap: ", BalanceUSDCAlice); 
        sw_bob.claim (swBobId, secret);
        BalanceUSDCAlice = usdc.balanceOf(alice); 
        //console.log("Alice USDC balance after swap: ", BalanceUSDCAlice);
        assertEq(BalanceUSDCAlice, depositAmountUSDC); // passes
        vm.stopPrank();

        vm.startPrank(bob); // Bob side
        uint256 BalanceOLASBob = olas.balanceOf(bob);         
        //console.log("Bob OLAS balance before swap: ", BalanceOLASBob);
        // secret from event sw_bob.claim (swBobId, secret); 
        sw_alice.claim(swAliceId, secret);
        BalanceOLASBob = olas.balanceOf(bob); 
        //console.log("Bob OLAS balance after swap: ", BalanceOLASBob);
        assertEq(BalanceOLASBob, depositAmountOLAS); // passes
        vm.stopPrank();

        vm.startPrank(alice); // Alice side
        vm.expectRevert();
        sw_alice.refund(swAliceId);
        vm.stopPrank();

        vm.startPrank(bob); // Bob side
        vm.expectRevert();
        sw_bob.refund(swBobId);
        vm.stopPrank();
    }

    // https://dev.to/rareskills/verify-signature-solidity-in-foundry-olj
    function testAliceDanContractSuccessRelay() public {
        // Impersonate the whale account for testing
        vm.startPrank(whale);
        //uint256 initialBalanceUSDC = usdc.balanceOf(whale); // Get the initial balance of whale
        //console.log("USDC initial balance: ", initialBalanceUSDC); // Log the final balance to the console
        uint256 transferAmountUSDC = 50000 * 10 ** usdc.decimals();
        uint256 depositAmountUSDC =  1000 * 10 ** usdc.decimals();
        usdc.transfer(dan, transferAmountUSDC);
        vm.stopPrank();

        vm.startPrank(bitget);
        //uint256 initialBalanceOLAS = olas.balanceOf(bitget); // Get the initial balance of whale
        //console.log("OLAS initial balance: ", initialBalanceOLAS); // Log the final balance to the console
        uint256 transferAmountOLAS = 50000 * 10 ** olas.decimals();
        uint256 depositAmountOLAS =  1000 * 10 ** olas.decimals();
        olas.transfer(alice, transferAmountOLAS);
        vm.stopPrank();

        bytes32 secret = bytes32(block.timestamp); // unsecure
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        uint256 expiration = block.timestamp + 3 * 60 * 60;
        uint256 deadline = block.timestamp + 3 * 60 * 60;

        vm.startPrank(alice); // Alice side
        olas.approve(address(sw_alice), depositAmountOLAS);
        uint256 swAliceId = sw_alice.newSwap(address(dan_safe), secretHash, expiration, olasAddress, depositAmountOLAS, true);
        //console.log(swAliceId);
        vm.stopPrank();

        vm.startPrank(dan); // Dan side
        usdc.approve(address(dan_safe), depositAmountUSDC); 
        /// pseudo secretHash from events -->
        uint256 swDanId = dan_safe.newSwap(address(sw_dan), alice, secretHash, expiration, usdcAddress, depositAmountUSDC, false);
        //console.log(swDanId);
        vm.stopPrank();

        vm.startPrank(alice); // Alice side
        uint256 BalanceUSDCAlice = usdc.balanceOf(alice);         
        //console.log("Alice USDC balance before swap: ", BalanceUSDCAlice); 
        sw_dan.claim (swDanId, secret);
        BalanceUSDCAlice = usdc.balanceOf(alice); 
        assertEq(BalanceUSDCAlice, depositAmountUSDC); // passes
        //console.log("Alice USDC balance after swap: ", BalanceUSDCAlice);
        vm.stopPrank();

        vm.startPrank(bob); // Dan side, call from Bob -> dan_safe
        uint256 BalanceOLASDan = olas.balanceOf(dan);         
        //console.log("Dan OLAS balance before swap: ", BalanceOLASDan);
        // secret from event sw_bob.claim (swBobId, secret);
        bytes32 msgHash = sw_alice.getMsgHash(address(dan_safe), swAliceId, secret, deadline);
        dan_safe.setSig(msgHash, 1, bytes32(uint256(uint160(address(dan_safe)))), 0); 
        // off-chain sign
        // false signature
        vm.expectRevert();
        dan_safe.claimRelay(address(sw_alice), swAliceId, secret, deadline, 0, bytes32(uint256(uint160(address(dan_safe)))), 0);
        // correct signature + buyer
        dan_safe.claimRelay(address(sw_alice), swAliceId, secret, deadline, 1, bytes32(uint256(uint160(address(dan_safe)))), 0);
        BalanceOLASDan = olas.balanceOf(address(dan_safe));
        assertEq(BalanceOLASDan, depositAmountOLAS); // passes 
        //console.log("Dan OLAS balance after swap: ", BalanceOLASDan);
        vm.stopPrank();

        vm.startPrank(alice); // Alice side
        vm.expectRevert();
        sw_alice.refund(swAliceId);
        vm.stopPrank();
    }

    function testAliceDanEOASuccessRelay() public {
        // Impersonate the whale account for testing
        vm.startPrank(whale);
        //uint256 initialBalanceUSDC = usdc.balanceOf(whale); // Get the initial balance of whale
        //console.log("USDC initial balance: ", initialBalanceUSDC); // Log the final balance to the console
        uint256 transferAmountUSDC = 50000 * 10 ** usdc.decimals();
        uint256 depositAmountUSDC =  1000 * 10 ** usdc.decimals();
        usdc.transfer(dan, transferAmountUSDC);
        vm.stopPrank();

        vm.startPrank(bitget);
        //uint256 initialBalanceOLAS = olas.balanceOf(bitget); // Get the initial balance of whale
        //console.log("OLAS initial balance: ", initialBalanceOLAS); // Log the final balance to the console
        uint256 transferAmountOLAS = 50000 * 10 ** olas.decimals();
        uint256 depositAmountOLAS =  1000 * 10 ** olas.decimals();
        olas.transfer(alice, transferAmountOLAS);
        vm.stopPrank();

        bytes32 secret = bytes32(block.timestamp); // unsecure
        bytes32 secretHash = sha256(abi.encodePacked(secret));
        uint256 expiration = block.timestamp + 3 * 60 * 60;
        uint256 deadline = block.timestamp + 3 * 60 * 60;

        vm.startPrank(alice); // Alice side
        olas.approve(address(sw_alice), depositAmountOLAS);
        uint256 swAliceId = sw_alice.newSwap(dan, secretHash, expiration, olasAddress, depositAmountOLAS, true);
        //console.log(swAliceId);
        vm.stopPrank();

        vm.startPrank(dan); // Dan side
        usdc.approve(address(sw_dan), depositAmountUSDC); 
        /// pseudo secretHash from events -->
        uint256 swDanId = sw_dan.newSwap(alice, secretHash, expiration, usdcAddress, depositAmountUSDC, false);
        //console.log(swDanId);
        vm.stopPrank();

        vm.startPrank(alice); // Alice side
        uint256 BalanceUSDCAlice = usdc.balanceOf(alice);         
        //console.log("Alice USDC balance before swap: ", BalanceUSDCAlice); 
        sw_dan.claim (swDanId, secret);
        BalanceUSDCAlice = usdc.balanceOf(alice); 
        assertEq(BalanceUSDCAlice, depositAmountUSDC); // passes
        //console.log("Alice USDC balance after swap: ", BalanceUSDCAlice);
        vm.stopPrank();

        vm.startPrank(bob); // Dan side, call from Bob
        uint256 BalanceOLASDan = olas.balanceOf(dan);         
        //console.log("Dan OLAS balance before swap: ", BalanceOLASDan);
        // secret from event sw_bob.claim (swBobId, secret);
        bytes32 msgHash = sw_alice.getMsgHash(dan, swAliceId, secret, deadline);
        // off-chain sign
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(privateKeyDan, msgHash);
        // expected revert with incorrect sig
        vm.expectRevert();
        sw_alice.claimRelay(swAliceId, secret, deadline, v, r, bytes32(uint256(s)-1)); 
        sw_alice.claimRelay(swAliceId, secret, deadline, v, r, s);
        BalanceOLASDan = olas.balanceOf(dan);
        assertEq(BalanceOLASDan, depositAmountOLAS); // passes 
        //console.log("Dan OLAS balance after swap: ", BalanceOLASDan);
        vm.stopPrank();

        vm.startPrank(alice); // Alice side
        vm.expectRevert();
        sw_alice.refund(swAliceId);
        vm.stopPrank();

        vm.startPrank(dan); // Dan side
        vm.expectRevert();
        sw_bob.refund(swDanId);
        vm.stopPrank();
    }
}
