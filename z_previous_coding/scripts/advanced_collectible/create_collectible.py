from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_shard
import time
STATIC_SEED = 123

def main():
    dev = accounts.add(config['wallets']['from_key'])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    transaction = advanced_collectible.createCollectible(
        STATIC_SEED, "None", {"from": dev})
    transaction.wait(1)
    requestId = transaction.events['requestedCollectible']['requestId']
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    time.sleep(45)
    shard = get_shard(advanced_collectible.tokenIdToShard(tokenId))
    print('Rejoice, oh traveler, for your offering of token {} has blessed you with {}. May the Gods continue to look over you and your quest to gather the lost shards.'.format(token_id, shard))
    