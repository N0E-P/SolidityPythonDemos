from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv


load_dotenv()
# permet d'importer dotenv directement dans le script


install_solc("0.6.0")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


print("Installing...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "": {"": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# installation de notre précédent code fait en solidity


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
    # Va prendre notre variable nommée compiled_sol. Et ça va l'envoyer dans le dossier compiled_code.json


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# on va chercher le bytecode que l'on cherche, a l'intérieur de chacun des fichiers nimés ci dessus. Dans le fichier compiled_code.json


abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# récupérer l'abi de la même manière que le bytecode ci dessus


# Sur le code final : récupérer l'abi de cette manière :
# abi = json.loads(
#    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
# )["output"]["abi"]


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# connect to Ganache to simulate a blockchain

chain_id = 1337

my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

private_key = os.getenv("PRIVATE_KEY")
# Se souvenir qu'il faut toujours ajouter "0x" devant l'adresse de sa clé privée sur Python, si on l'écrit directement dans le script.
# Mais ce n'est pas recommandé du tout d'écrire sa clé privé dans le code.
# Donc, on va la récupérer en écrivant : os.getenv("PRIVATE_KEY")


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# création du contract
nonce = w3.eth.getTransactionCount(my_address)
# Aller voir la dernière transaction, pour y récupérer le nonce (égal au nombre de transactions déjà faites)


transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# signer la transaction

print("Deployint contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# envoyer la transaction

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed!")
# fait en sorte que le code s'arrete momentanément, en attendant que la transaction réussise


# WORKING WITH THE CONTRACT :
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Création du contract (contract address + contract ABI)
# in general, when we look for a contract ABI, we can just google it to find it

print(simple_storage.functions.retrieve().call())
# Initial value of favorite number

print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
    # On écrit +1 après nonce car le premier nonce est déjà utilisé pour la première transaction
    # un nonce ne peut etre utilisé qu'une seule fois par transactions
)
# Création de la transaction

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# On signe la transaction

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# On envoie la transaction

tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Contract updated!")
# fait en sorte que le code s'arrete momentanément, en attendant que la transaction réussise

print(simple_storage.functions.retrieve().call())
# Nouvelle valeur de favorite number


# probleme : ligne 1 : il trouve pas solc ou solcX
# Alors qu'avant, ça marchais très bien


tx.wait(1)
# ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
