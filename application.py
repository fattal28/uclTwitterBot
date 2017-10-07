import json
import tweepy

from flask import Flask, request
from make_string import tweet_text

app = Flask(__name__)

with open("secret.json", "r") as f:
    secret = json.load(f)
    webhook_secret = secret["webhook_secret"]

auth = tweepy.OAuthHandler(secret['consumer_key'], secret['consumer_secret'])
auth.set_access_token(secret['access_token_key'], secret['access_token_secret'])

twitter = tweepy.API(auth)

def society(str):
    return bool(re.search(r"(Club|Society|Application of Psychedelics|Chinese Students and Scholars Association|Christian Union|Effective Altruism|European Law Students Association|Guild|Hiking & Walking|Kinesis Magazine|Law for All|Pi Media|Pole Fitness|Red Star FC|SAVAGE Journal|Snooker and Pool|Student Action for Refugees|TherouxSoc)", str))

@app.route("/", methods=["POST"])
def index():
    request_data = json.loads(request.get_data())

    if request_data["name"] == "challenge":
        print("Responding to challenge")
        challenge = json.loads(request.get_data())["challenge"]
        return json.dumps({"challenge": challenge})

    elif request_data["name"] == "bookings_changed":
        with open("tweets.json", "r") as f:
            tweets = json.load(f)

        for x in request_data["content"]["bookings_added"]:
            if society(x["contact"]):
                twitter.update_status(tweet_text(x))
                tweets.append(tweet_text(x))

        with open("tweets.json", "w") as f:
            json.dump(tweets, f)

    return ""
