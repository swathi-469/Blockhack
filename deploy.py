"""
deploy.py: script for deploying a smart contract on Ropsten chain
"""
import json
import config
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

def deploy():
    # web3.py instance
    w3 = Web3(HTTPProvider(config.ROPSTEN_API))
    print("w3 is connected: ", w3.isConnected())

    # get account (personal for now)
    key = "0x" + config.PRIVATE_KEY
    acct = w3.eth.account.privateKeyToAccount(key)

    # load the reward contract
    truffle_reward_file = json.load(open('./build/contracts/Reward.json'))
    reward_abi = truffle_reward_file['abi']
    reward_bytecode = truffle_reward_file['bytecode']
    reward_contract= w3.eth.contract(bytecode=reward_bytecode, abi=reward_abi)

    # load the levelpass contract
    truff_levelpass_file = json.load(open('./build/contracts/LevelPass.json'))
    levelpass_abi = truff_levelpass_file['abi']
    levelpass_bytecode = truff_levelpass_file['bytecode']
    levelpass_contract= w3.eth.contract(bytecode=levelpass_bytecode, abi=levelpass_abi)

    # building transaction for reward
    reward_contract_txn = reward_contract.constructor().buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})

    # building transaction for levelpass
    levelpass_contract_txn = levelpass_contract.constructor().buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})

    # sign transactions
    reward_signed = acct.signTransaction(reward_contract_txn)
    levelpass_signed = acct.signTransaction(levelpass_contract_txn)

    # deploy contracts on chain
    reward_hash = w3.eth.sendRawTransaction(reward_signed.rawTransaction)
    levelpass_hash = w3.eth.sendRawTransaction(levelpass_signed.rawTransaction)
    reward_receipt = w3.eth.waitForTransactionReceipt(reward_hash)
    levelpass_receipt = w3.eth.waitForTransactionReceipt(levelpass_hash)

    # save addresses in config (temp, idk how this should actually work)
    config.REWARD_CONTRACT_ADDRESS = reward_receipt['contractAddress']
    config.LEVELPASS_CONTRACT_ADDRESS = levelpass_receipt['contractAddress']
    print("Reward Contract Deployed At:", reward_receipt['contractAddress'])
    print("LevelPass Contract Deployed At: ", levelpass_receipt['contractAddress'])

if __name__ == "__main__":
    deploy()