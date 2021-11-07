"""
helpers.py: helper functions
"""
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
import config

# initializeRewardContract(): helper function that gets w3, reward contract, account
def initializeRewardContract(user, json):
    # get the abi
    truffleFile = json.load(open(json))
    abi = truffleFile['abi']

    # get the contract address and create acct
    w3 = Web3(HTTPProvider(config.ROPSTEN_API))
    contract = w3.eth.contract(config.REWARD_CONTRACT_ADDRESS, abi=abi)
    acct = w3.eth.account.privateKeyToAccount(user['private_key'])
    return (w3, contract, acct)

# initializeLevelPassCOntract(): helper function that gets w3, level pass contract, account
def initializeLevelPassContract(user, json):
    # get the abi
    truffleFile = json.load(open(json))
    abi = truffleFile['abi']

    # get the contract address and create acct
    w3 = Web3(HTTPProvider(config.ROPSTEN_API))
    contract = w3.eth.contract(config.LEVELPASS_CONTRACT_ADDRESS, abi=abi)
    acct = w3.eth.account.privateKeyToAccount(user['private_key'])
    return (w3, contract, acct)