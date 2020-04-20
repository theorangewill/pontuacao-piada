import tweepy
import logging
import os

home = os.path.dirname(os.path.realpath(__file__))
consumer_key = (open(home+"/private/consumer_key", "r")).read()[:-1]
consumer_secret = (open(home+"/private/consumer_secret", "r")).read()[:-1]
access_token = (open(home+"/private/access_token", "r")).read()[:-1]
access_token_secret = (open(home+"/private/access_token_secret", "r")).read()[:-1]

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(home+"/log/main.log")
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)5s] - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)



mentions = api.mentions_timeline()

for mention in mentions:
    id = mention.id
    tweet = mention.text
    user = mention.user.screen_name
    userid = mention.user.id
    piada = mention.in_reply_to_status_id
    print(user)
    print(tweet)
    #print(tweet)
