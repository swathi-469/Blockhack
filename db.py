"""
Mock user information to be updated by backend
"""
import config

user = {
    'name': 'Michael Jackson',
    'level_pass_id' : 0,
    'private_key' : None,
    'reward_uris' : [214124124214],
    'thresholds' : {214124124214 : 300},
    'progress': 0,
    'recent_location':['Panda Express']
}

"""
Below are dictionaries that act as a temporary database for our backend
All NFTs are unique, so the dictionaries below should be one-to-one
"""
# rewardIdToIdx: translation from a rewardId to a rewardIdx
rewardIdToIdx = {

}

# rewardIdToURI: translation from a rewardId to a URI
rewardIdToURI = {

}

# levelPassIdtoURI: translation from a levelPassId to a URI
levelPassIdToURI = {

}