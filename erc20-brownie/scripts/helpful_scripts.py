from brownie import network, config, accounts

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]


def get_account():
    accounts.load("chaussette")
    return accounts[0]
