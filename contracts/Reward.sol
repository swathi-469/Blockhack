pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract Reward is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    event RewardRequest(uint256 id);

    constructor()
        public
        ERC721("Reward", "RWD")
    {   }

    /* requestNewReward(): requests a new reward NFT and gives it to the specified recipient address
     */
    function requestNewReward(
        address recipient,
        string memory tokenURI
    ) public {
        _tokenIds.increment();
        uint256 newId = _tokenIds.current();
        _mint(recipient, newId);
        _setTokenURI(newId, tokenURI);
        emit RewardRequest(newId);
    }

    /* consumeReward(): consumes a reward, essentially burning the NFT
     */
    function consumeReward(
        uint256 rewardId
    ) public {
        _burn(rewardId);
    }
}
