from brownie import SimpleStorage, accounts


def test_deploy():
    # arranging
    account = accounts[0]

    # acting
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # asserting
    assert starting_value == expected


def test_updating_storage():
    # arranging
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # acting
    expected = 15
    simple_storage.store(expected, {"from": account})

    # asserting
    assert expected == simple_storage.retrieve()
