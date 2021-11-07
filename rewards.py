"""
rewards.py: logic for sending transactions and interactions with Reward contract
"""
import json
from helpers import initializeRewardContract
import config

# getNewReward(): gets a new reward for the specified user with the passed in URI
# returns the token id of the new reward nft
def getNewRewardFromChain(user, uri):
    w3, contract, acct = initializeRewardContract(user, './build/contracts/Reward.json')

    # Perform transaction, essentially give a new nft to
    tx = contract.functions.requestNewReward(acct.address, uri).buildTransaction({
        'nonce': w3.eth.getTransactionCount(acct.address)
    })
    signed_tx = w3.eth.account.signTransaction(tx, user['private_key'])
    hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # get the id of the requested reward (return is in hex base 16)
    return int(w3.eth.getTransactionReceipt(hash)['logs']['0']['data'], 16)

# deleteRewardFromChain(): deletes the specified reward id from the chain
def deleteRewardFromChain(user, reward_id):
    w3, contract, acct = initializeRewardContract(user, './build/contracts/Reward.json')

    # Perform transaction, burn (delete the nft)
    tx = contract.functions.consumeReward(reward_id).buildTransaction({
        'nonce': w3.eth.getTransactionCount(acct.address)
    })
    signed_tx = w3.eth.account.signTransaction(tx, user['private_key'])
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)

# getRewardURI(): gets the URI associated with a specified reward id
def getRewardURI(user, reward_id):
    w3, contract, acct = initializeRewardContract(user, './build/contracts/Reward.json')

    # get uri (doesn't require transaction)
    return contract.functions.tokenURI(reward_id).call()