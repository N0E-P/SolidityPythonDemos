// contracts/NoeToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract NoeToken is ERC20 {
    // wei
    constructor(uint256 initialSupply) ERC20("NoeToken", "NOE") {
        _mint(msg.sender, initialSupply);
    }
}
