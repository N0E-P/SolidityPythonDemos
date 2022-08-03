from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    # -1 est pour choisir le contract le plus récent que l'on a créé
    print(simple_storage.retrieve())


def main():
    read_contract()
