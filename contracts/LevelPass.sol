pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract LevelPass is ERC721URIStorage, Ownable {
    using Strings for string;
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;

    mapping(address => uint256) userToId;
    mapping(uint256 => uint256[]) idToRewards;

    event LevelPassRequest(uint256 id);
    event AddedReward(uint256 idx);
    event RemovedReward(uint256 id);
    event GetTokenURI(string uri);

    constructor()
        public
        ERC721("LevelPass", "LP")
    {   }

    /* requestNewLevelPass(): creates a new level pass, sets its URI, and transfers it to the recipient
     */
    function requestNewLevelPass(
        address recipient,
        string memory tokenURI
    ) public {
        require(
            userToId[recipient] == 0,
            "Recipient already owns a level pass."
        );
        _tokenIds.increment();
        uint256 newId = _tokenIds.current();
        _mint(recipient, newId);
        _setTokenURI(newId, tokenURI);
        userToId[recipient] = newId;
        emit LevelPassRequest(newId);
    }

    /* addRewardToLevelPass(): adds a reward to the specified LevelPass, returns the index of the added pass
     */
    function addRewardToLevelPass(
        uint256 levelPassId,
        uint256 rewardId
    ) public {
        idToRewards[levelPassId].push(rewardId);
        emit AddedReward(idToRewards[levelPassId].length - 1);
    }

    /* removeRewardFromLevelPass(): removes a reward from the specified LevelPass, returning the id of the reward that was removed
     */
    function removeRewardFromLevelPass(
        uint256 levelPassId,
        uint256 rewardIdx // same idx as returned from addRewardToLevelPass()
    ) public {
        uint256 rewardId = idToRewards[levelPassId][rewardIdx];
        delete idToRewards[levelPassId][rewardIdx];
        emit RemovedReward(rewardId);
    }

    /* getRewards(): gets the rewards for a specified LevelPass
     */
    function getRewards(
        uint256 levelPassId
    ) public view returns (uint256[] memory) {
        return idToRewards[levelPassId];
    }
}

