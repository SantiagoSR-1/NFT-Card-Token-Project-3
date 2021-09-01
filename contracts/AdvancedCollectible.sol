pragma solidity ^0.6.6;

import "@openzepplin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {

    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public tokenCounter;

    // Allow for variation to exist in minting process, thereby increasing collectibality or creating artificial rarity
    enum Shard{
        Black_Lotus_01_16,
        Black_Lotus_02_16, 
        Black_Lotus_03_16, 
        Black_Lotus_04_16, 
        Black_Lotus_05_16, 
        Black_Lotus_06_16, 
        Black_Lotus_07_16, 
        Black_Lotus_08_16, 
        Black_Lotus_09_16, 
        Black_Lotus_10_16,
        Black_Lotus_11_16, 
        Black_Lotus_12_16, 
        Black_Lotus_13_16, 
        Black_Lotus_14_16, 
        Black_Lotus_15_16, 
        Black_Lotus_16_16, 
        Mox_Emerald_01_16,
        Mox_Emerald_02_16,
        Mox_Emerald_03_16,
        Mox_Emerald_04_16,
        Mox_Emerald_05_16,
        Mox_Emerald_06_16,
        Mox_Emerald_07_16,
        Mox_Emerald_08_16,
        Mox_Emerald_09_16,
        Mox_Emerald_10_16,
        Mox_Emerald_11_16,
        Mox_Emerald_12_16,
        Mox_Emerald_13_16,
        Mox_Emerald_14_16,
        Mox_Emerald_15_16,
        Mox_Emerald_16_16,
        }

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Shard) public tokenIdToShard;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestCollectible(bytes32 indexed requestId);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("MagicTheGathering", "MTG")
    {
        keyHash = _keyhash;
        // 0.1 LINK or 1,000,000,000,000,000,000
        fee = 0.1 * 10 ** 18; 
        tokenCounter = 1;
    }

    function createCollectible(uint256 userProvidedSeed, string memory tokenURI) public
    public returns (bytes32)
    {
        bytes32 requestId = requestRandomness(keyHash, fee, userProvidedSeed);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override{
        address magicOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(magicOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);
        // Select shard from scale of 1 to 32. 01 - 16 are designated for card #1, and 17 - 32 are designated for card #2.
        Shard shard = Shard(randomNumber % 32); 
        tokenIdToShard[newItemId] = shard;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public{
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
