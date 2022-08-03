# from turtle import update
# il y a ça qui est arrivé ici tout seul

from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    # va utiliser la fonction get_account, pour savoir si l'on utilise un réseau de developpement, de test, ou un mainnet
    simple_storage = SimpleStorage.deploy({"from": account})
    # déploie le contract (extrèmement plus simple que de tout écrire manuellement en utilisant seulement ganache)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    # contract interaction with brownie
    transaction.wait(1)
    # on attend qu'un bloc ait été validé avant de passer a la suite du programme
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    # permet de savoir si l'on utilise un réseau de developpement, de test, ou un mainnet


def main():
    deploy_simple_storage()
