from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

cow_metadata_dic = {
    "BERNARD": "https://ipfs.io/ipfs/QmPAMhE49iukQve1zySWBdHM1QNuVUVBf99ivk4mmyeNtN?filename=0-BERNARD.json",
    "ROGER": "https://ipfs.io/ipfs/QmURwosEikLggRzQED7Ndeg9Lmts8xNWDeSvoszHPPt9M5?filename=1-ROGER.json",
    "MARGUERITE": "https://ipfs.io/ipfs/QmPKFc7Pnrj1PcoUmMERBXN9hQrQCBWk46vQ8v5UaKgZnM?filename=2-MARGUERITE.json",
    "KEVIN": "https://ipfs.io/ipfs/QmW6t8Wq82Uu9gVavYichAu9vF1E1HH8bZoMXtJHEnA9sk?filename=1-KEVIN.json",
    "TITOUAN": "https://ipfs.io/ipfs/QmT51XLjRYN9WkaNwcM4j3oXhucC7mYpjH2q5PTxe5FZMF?filename=0-TITOUAN.json",
    "JOSELINE": "https://ipfs.io/ipfs/QmUJab9EhFwbZQoW2SBPgeeHYk7hpLtAwEH8bofVuMWHx8?filename=2-JOSELINE.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, cow_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
