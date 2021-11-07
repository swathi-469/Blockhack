"""
levelpass.py: logic for sending transactions and interactions with Reward contract
"""
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from helpers import initializeLevelPassContract
import config

# getNewLevelPassFromChain(): creates a new nft and gives it the current user
def getNewLevelPassFromChain(user, uri):
    w3, contract, acct = initializeLevelPassContract(user, './build/contracts/LevelPass.json')

    # Perform transaction, essentially give a new nft to
    tx = contract.functions.requestNewLevelPass(acct.address, uri).buildTransaction({
        'nonce': w3.eth.getTransactionCount(acct.address)
    })
    signed_tx = w3.eth.account.signTransaction(tx, user['private_key'])
    hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # get the id of the requested reward (return is in hex base 16)
    return int(w3.eth.getTransactionReceipt(hash)['logs']['0']['data'], 16)

# addRewardToLevelPass(): adds a reward to the level pass (note that this changes contract state, doesn't actually give new nft)
# returns the INDEX of the inserted reward in the mapping
def addRewardToLevelPass(user, levelPassId, rewardId):
    w3, contract, acct = initializeLevelPassContract('./build/contracts/LevelPass.json')

    tx = contract.functions.requestNewLevelPass(levelPassId, rewardId).buildTransaction({
        'nonce': w3.eth.getTransactionCount(acct.address)
    })
    signed_tx = w3.eth.account.signTransaction(tx, user['private_key'])
    hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return int(w3.eth.getTransactionReceipt(hash)['logs']['0']['data'], 16)

# removeRewardFromLevelPass(): removes a reward from the level pass and returns the ID of the removed reward
# does not burn an NFT, rather it just changes smart contract state
def removeRewardFromLevelPass(user, levelPassId, rewardIdx):
    w3, contract, acct = initializeLevelPassContract(user, './build/contracts/LevelPass.json')

    tx = contract.functions.removeRewardFromLevelPass(levelPassId, rewardIdx).buildTransaction({
        'nonce': w3.eth.getTransactionCount(acct.address)
    })
    signed_tx = w3.eth.account.signTransaction(tx, user['private_key'])
    hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    return int(w3.eth.getTransactionReceipt(hash)['logs']['0']['data'], 16)

# getAllRewards(): gets all rewards for a certain LevelPass, returns list of rewardIds
def getAllRewards(user, levelPassId):
    # get contract for LevelPass
    w3, levelpass_contract, acct = initializeLevelPassContract(user, './build/contracts/LevelPass.json')

    # store all URIs for rewards
    rewardIds = []

    # get array of reward IDs
    # TODO: FIND OUT WHAT THIS RETURNS AND CHANGE TO ARRAY IF NEEDED
    rewards =  levelpass_contract.functions.getRewards(levelPassId).call()

    # iterate through rewards and add URIs
    for rew in rewards:
        rewardIds.append(rew)

    # return reward URIs
    return rewardIds
    
# getLevelPassURI(): gets the URI for a certain LevelPass
def getLevelPassURI(user, levelPassId):
    w3, contract, acct = initializeLevelPassContract(user, './build/contracts/Reward.json')
    return contract.functions.tokenURI(levelPassId).call()