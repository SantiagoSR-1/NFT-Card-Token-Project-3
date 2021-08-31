from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_shard
from pathlib import Path
import os
import requests
import json

shard_to_image_uri = {
    "B_L-01.16": "https://gateway.pinata.cloud/ipfs/QmZFVJuTs9BajSTYXVKYvajDuHWCxQyg7hxw9kRypUEu3f/Black_Lotus-01-16.png",
    "B_L-02.16": "https://gateway.pinata.cloud/ipfs/QmZMuwmggxxcyGirmkByAXjmEXQPBDDymmvMpzuzH22Tmw/Black_Lotus-02-16.png",
    "B_L-03.16": "https://gateway.pinata.cloud/ipfs/QmQavH63cgjMd5vkJNLoxRpPdC1jSYs9YQATPzeMyQU9po/Black_Lotus-03-16.png",
    "B_L-04.16": "https://gateway.pinata.cloud/ipfs/QmZcZjAVTxYbGF4xScd6uZgBZBXa3bSqEQf72M7TZrnwsw/Black_Lotus-04-16.png",
    "B_L-05.16": "https://gateway.pinata.cloud/ipfs/QmeebrbGKsebcjFZ6fcL8X8MaMx5bMBcvSA3AyVKWaNSWR/Black_Lotus-05-16.png",
    "B_L-06.16": "https://gateway.pinata.cloud/ipfs/QmWwsJoPTJQ9RB2A9YWcEusYKiW56vYors1AUS6Vo4iVw9/Black_Lotus-06-16.png",
    "B_L-07.16": "https://gateway.pinata.cloud/ipfs/QmRdahUiFaJiiShKEfCpAmyyHPMb3Z2ybGJdwJta56JKZJ/Black_Lotus-07-16.png",
    "B_L-08.16": "https://gateway.pinata.cloud/ipfs/QmeVgGPoqC42Yj8G9RtyGnH3xkst3aFgpQC8SsNqpN6y28/Black_Lotus-08-16.png",
    "B_L-09.16": "https://gateway.pinata.cloud/ipfs/QmaFrhaRK1HRcbgYMTuuo3V6rxKtgPCzP14DyHskQ8nuo8/Black_Lotus-09-16.png",
    "B_L-10.16": "https://gateway.pinata.cloud/ipfs/QmTukb7axaUSskN9FTBHkL9deEy4XwapdkR4XA5yrNiD54/Black_Lotus-10-16.png",
    "B_L-11.16": "https://gateway.pinata.cloud/ipfs/QmTD5XpibzQKGs9QUVQBaUwvwjV3oKRvbxKzGshaH22LaD/Black_Lotus-11-16.png",
    "B_L-12.16": "https://gateway.pinata.cloud/ipfs/QmZdKBCoUJznrfWoUTLLsuAFywHu7Xbu9goZ5qFyRqVEWd/Black_Lotus-12-16.png",
    "B_L-13.16": "https://gateway.pinata.cloud/ipfs/Qmb1KZEJq2zQ2qVkkeuHG8SzgXkj6bB2HrsP2sPeEXAR8F/Black_Lotus-13-16.png",
    "B_L-14.16": "https://gateway.pinata.cloud/ipfs/QmTzBh788gk2w1t7f1iVNuKwPoKvkBGK3YKcKy7yJvhcfL/Black_Lotus-14-16.png",
    "B_L-15.16": "https://gateway.pinata.cloud/ipfs/QmXZEBQNjWW5nmFobXuKAXWohrxviSCSfhEwNeGTL3oxVh/Black_Lotus-15-16.png",
    "B_L-16.16": "https://gateway.pinata.cloud/ipfs/QmdXjLwD9n7WJ1xvHnbbgHXkpLemjnbaiiCn5U9W8TJLYM/Black_Lotus-16-16.png",
    "M_E-01.16": "https://gateway.pinata.cloud/ipfs/QmXyJhRqDCiExpWt7MBKo8LZZVZqqdFSJKSZscax2L2HtL/Mox_Emerald-01-16.png",
    "M_E-02.16": "https://gateway.pinata.cloud/ipfs/QmafKh4vLDn3mEwjF963nwiJGXddXg7QxGQSLzcT8MQgGV/Mox_Emerald-02-16.png",
    "M_E-03.16": "https://gateway.pinata.cloud/ipfs/QmZntaRoCUU77oVsctKw6TMnb6QQL3SNTTSH6xFygAhLn8/Mox_Emerald-03-16.png",
    "M_E-04.16": "https://gateway.pinata.cloud/ipfs/QmcNd2xpaQn5XBMiyZjmXTpwCYAUDLWz3h5NhSa3DkVgW1/Mox_Emerald-04-16.png",
    "M_E-05.16": "https://gateway.pinata.cloud/ipfs/QmRfU2a7kGifRdA1X55jg43M1xCR9KGAAD7jZfXfWerSBd/Mox_Emerald-05-16.png",
    "M_E-06.16": "https://gateway.pinata.cloud/ipfs/QmU6ktXeH7hr4QXHaKTs75cQEcpvnJPjvAYueP9kSTfnAm/Mox_Emerald-06-16.png",
    "M_E-07.16": "https://gateway.pinata.cloud/ipfs/QmVqb3ZhioRX9kmcCbhNXq51PcMgeoyBgNUjBCrHL8Tgyh/Mox_Emerald-07-16.png",
    "M_E-08.16": "https://gateway.pinata.cloud/ipfs/QmQC226tzfCCvEvhxCTknPwQzyBDMfyhrGM9rHL2G5TaDx/Mox_Emerald-08-16.png",
    "M_E-09.16": "https://gateway.pinata.cloud/ipfs/QmTbgAxrvW8wqkF8w4oPvqkYEfjswnZX51p1FDeEuW5taU/Mox_Emerald-09-16.png",
    "M_E-10.16": "https://gateway.pinata.cloud/ipfs/QmdA66q7NPjruVBZf8S1fQDSTjrTb7SXz9wWS2jFKjKste/Mox_Emerald-10-16.png",
    "M_E-11.16": "https://gateway.pinata.cloud/ipfs/QmPmVrGAcy1fehFMHC121yhg4a7sKNXqkGhKw8Ha7iZBUy/Mox_Emerald-11-16.png",
    "M_E-12.16": "https://gateway.pinata.cloud/ipfs/QmdCgXieyeAbr2ifVpLyHfQ2jTajTXogWMdnYW3TfTW4pQ/Mox_Emerald-12-16.png",
    "M_E-13.16": "https://gateway.pinata.cloud/ipfs/QmX5PVnqfoSf7RM7xuZNZ9vErrGay4pKsxhbZx6CSvp5WQ/Mox_Emerald-13-16.png",
    "M_E-14.16": "https://gateway.pinata.cloud/ipfs/QmXRnf31byN7CSassWktueezFJ2amPMCbredmy4QXSNPHe/Mox_Emerald-14-16.png",
    "M_E-15.16": "https://gateway.pinata.cloud/ipfs/Qmerck1bA5wjH8LhFVrwSA6AFxLQX191yj4wahz1WetLRd/Mox_Emerald-15-16.png",
    "M_E-16.16": "https://gateway.pinata.cloud/ipfs/QmUXAWXUGMTKxvim6Kdr7EgVginQzXPF1acz98axqQBLwE/Mox_Emerald-16-16.png",
}
def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) -1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        shard = get_shard(nft_contract.tokenIdToShard(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(token_id)
            + "-" + shard + ".json"
        )
        #./metadata/kovan/0-IMAGE.json
        if Path(metadata_file_name).exists():
            print("{} already exists".format(metadata_file_name))
        else:
            print("Creating metadata file {}".format(metadata_file_name))
            collectible_metadata["name"] = get_shard(
                nft_contract.tokenIdToShard(token_id)
            )
            collectible_metadata["description"] = "Fortune has blessed you with {}. Seek out the other shards of this set to unlock this card's true potential".format(
                collectible_metadata["name"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    shard.lower().replace("_", "-"))
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = shard_to_image_uri[shard] if not image_to_upload
            else  image_to_upload
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, 'w') as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# http://127.0.0.1:5001
# curl -X POST -F file=@img/xxx.png http://localhost:5001/api/v0/add

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        response = requests.post(
            ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename
        )
        print(uri)
        return uri
    return None