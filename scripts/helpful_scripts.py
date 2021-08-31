from brownie import AdvancedCollectible, accounts, config, interface, network

def get_shard(shard_number):
    switch = {
        0: 'Black Lotus - Shard #01 of 16', 
        1: 'Black Lotus - Shard #02 of 16', 
        2: 'Black Lotus - Shard #03 of 16', 
        3: 'Black Lotus - Shard #04 of 16', 
        4: 'Black Lotus - Shard #05 of 16', 
        5: 'Black Lotus - Shard #06 of 16', 
        6: 'Black Lotus - Shard #07 of 16', 
        7: 'Black Lotus - Shard #08 of 16', 
        8: 'Black Lotus - Shard #09 of 16', 
        9: 'Black Lotus - Shard #10 of 16',
        10: 'Black Lotus - Shard #11 of 16',
        11: 'Black Lotus - Shard #12 of 16',
        12: 'Black Lotus - Shard #13 of 16',
        13: 'Black Lotus - Shard #14 of 16',
        14: 'Black Lotus - Shard #15 of 16',
        15: 'Black Lotus - Shard #16 of 16',
        16: 'Mox Emerald - Shard #01 of 16',
        17: 'Mox Emerald - Shard #02 of 16',
        18: 'Mox Emerald - Shard #03 of 16',
        19: 'Mox Emerald - Shard #04 of 16',
        20: 'Mox Emerald - Shard #05 of 16',
        21: 'Mox Emerald - Shard #06 of 16',
        22: 'Mox Emerald - Shard #07 of 16',
        23: 'Mox Emerald - Shard #08 of 16',
        24: 'Mox Emerald - Shard #09 of 16',
        25: 'Mox Emerald - Shard #10 of 16',
        26: 'Mox Emerald - Shard #11 of 16',
        27: 'Mox Emerald - Shard #12 of 16',
        28: 'Mox Emerald - Shard #13 of 16',
        29: 'Mox Emerald - Shard #14 of 16',
        30: 'Mox Emerald - Shard #15 of 16',
        31: 'Mox Emerald - Shard #16 of 16'
        }
    return switch[shard_number]

def fund_advanced_collectible(nft_contract):
    dev = accounts.add(config['wallets']['from_key'])
    link_token = interface.LinkTokenInterface(
        config['networks'][network.show_active()]['link_token'])
    link_token.transfer(nft_contract, 1000000000000000000, {"from": dev})
