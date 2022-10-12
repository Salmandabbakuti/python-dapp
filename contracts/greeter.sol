//SPDX-License-Identifier: MIT
pragma solidity 0.8.16;

contract Greeter {
    string greeting = "Hello Web3 Devs!";

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
