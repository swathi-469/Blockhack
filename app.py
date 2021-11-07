"""
api.py: defines routes for app
"""
import flask
import config
from db import user, rewardIdToIdx, rewardIdToURI, levelPassIdToURI
import json
from flask import jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Home route
@app.route("/")
# @app.route("/<path:path>")
def hello_world():
    """
    Root route for our Flask app API.
    """
    return '<img src="https://i.kym-cdn.com/photos/images/original/001/211/814/a1c.jpg" alt="cowboy" />'
@app.route('/bc/', methods=['GET'])
def home():
    # get the current rewards that the user has (cached in db)
    rewards_uris = user['reward_uris']

    # display these rewards
    return jsonify({"rewards": rewards_uris})
        

# Route to unlock reward if available, else show how much more progress until next reward
@app.route('/bc/unlock', methods=['GET'])
def unlock_rewards():
    # generate a reward
    # TODO: replace with db or blockchain
    rewards = []
    progress = user['progress']
    if len(user['reward_uris']) == 0:
        return jsonify({"error": "No reward available"})
    for i in user['reward_uris']:
        if user['thresholds'][i] <= user['progress']:
            rewards.append(i)
        else:
            progress = min(progress, user['thresholds'][i] - user['progress'])
    return jsonify({'progress':progress, 'rewards': rewards})        


# Route for payment, should get user data from payment
@app.route('/bc/pay', methods=['POST'])
def pay():
    data = request.form
    location = data.get('location')
    payment = data.get('payment')
    # TODO: replace with db or blockchain
    user["progress"] += payment
    user["recent_location"].append(location)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
