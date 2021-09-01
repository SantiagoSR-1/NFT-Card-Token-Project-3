from brownie import AdvancedCollectible, network, accounts, config
from scripts.helpful_scripts import get_shard


shard_metadata_dictionary = {
    "Black_Lotus_01_16": "https://",
    "Black_Lotus_02_16": "https://",
    "Black_Lotus_03_16": "https://",
    "Black_Lotus_04_16": "https://",
    "Black_Lotus_05_16": "https://",
    "Black_Lotus_06_16": "https://",
    "Black_Lotus_07_16": "https://",
    "Black_Lotus_08_16": "https://",
    "Black_Lotus_09_16": "https://",
    "Black_Lotus_10_16": "https://",
    "Black_Lotus_11_16": "https://",
    "Black_Lotus_12_16": "https://",
    "Black_Lotus_13_16": "https://",
    "Black_Lotus_14_16": "https://",
    "Black_Lotus_15_16": "https://",
    "Black_Lotus_16_16": "https://",
    "Mox_Emerald_01_16": "https://",
}

def main():
    print("Working on" + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print("The number of tokens deployed is: "
        + str(number_of_advanced_collectibles)
        )
    for token_id in range(number_of_advanced_collectibles):
        shard = get_shard(advanced_collectible.tokenIdToShard(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, shard_metadata_dictionary[shard])
        else:
            print("Error: tokenURI {} already exists".format(token_id))
    
def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Your NFT is availble for viewing. Please visit {}".format(
            ## What will we be using to host the information?
        )
    )
    print("Allow for up to 20 minutes for the minting process. Select the "refresh metadata" prompt when asked.")
adf