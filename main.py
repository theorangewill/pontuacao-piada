import tweepy
import logging
import os
import re
import datetime

home = os.path.dirname(os.path.realpath(__file__))
consumer_key = (open(home+"/private/consumer_key", "r")).read().strip('\n')
consumer_secret = (open(home+"/private/consumer_secret", "r")).read().strip('\n')
access_token = (open(home+"/private/access_token", "r")).read().strip('\n')
access_token_secret = (open(home+"/private/access_token_secret", "r")).read().strip('\n')

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(home+"/log/main.log")
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)7s] - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

SCORE_FILE = home+"/score"
LASTMENTION_FILE = home+"/lastmention"

scorefiles = [f for f in os.listdir('.') if re.match(r'\S+.score', f)]

scoreboards = {}
for scorefile in scorefiles:
    scores = open(scorefile, "r").read().strip('\n').split('\n')
    scoreboards[re.sub(r'.score','',scorefile)] = {}
    try:
        scoreboards[re.sub(r'.score','',scorefile)] = dict([i.split(';') for i in scores])
    except ValueError:
        logger.error("Maybe this file is empty or ';' is missing - " + scorefile)

if os.path.isfile(LASTMENTION_FILE):
    lastmention = (open(LASTMENTION_FILE, "r")).read().strip('\n')
else:
    lastmention = 0

mentions = api.mentions_timeline()
changed = False

for mention in mentions:
    id = str(mention.id)
    tweet = str(mention.text)
    master = str(mention.user.screen_name)
    masterid = str(mention.user.id)
    jokeid = str(mention.in_reply_to_status_id)
    joke = str(api.get_status(joke).text)
    player = str(api.get_status(joke).user.screen_name)
    playerid = str(api.get_status(joke).user.id)

    if lastmention == id:
        break
    elif not changed:
        lastmention = id
        changed = True
        (open(LASTMENTION_FILE, "w")).write(str(id))


    try:
        points = int(re.sub('\@\S+', '', tweet).strip().split(';')[0])
        print(int(points))

        if masterid in scoreboards.keys():
            if playerid in scoreboards[masterid].keys():
                scoreboards[masterid][playerid] = int(scoreboards[masterid][playerid]) + int(points)
                logger.info("Added "+str(points) + " points for the joke \"" + str(joke) + "("+str(jokeid)") to player @" + str(player) + " of master @"+ str(master) + " with total of " + str(scoreboards[masterid][playerid]) + " points")
            else:
                scoreboards[masterid][playerid] = int(points)
                logger.info("New player added to @" + str(master) + ": @" + str(player) + "("+str(playerid)+")")
                logger.info("Added "+str(points) + " points for the joke \"" + str(joke) + "("+str(jokeid)") to player @" + str(player) + " of master @"+ str(master) + " with total of " + str(scoreboards[masterid][playerid]) + " points")
        else:
            scoreboards[masterid] = {}
            scoreboards[masterid][playerid] = int(points)
            logger.info("New master added: @" + str(master) + "(" + str(masterid) + ")")
            logger.info("New player added to @" + str(master) + ": @" + str(player) + "("+str(playerid)+")")
            logger.info("Added "+str(points) + " points for the joke \"" + str(joke) + "("+str(jokeid)") to player @" + str(player) + " of master @"+ str(master) + " with total of " + str(scoreboards[masterid][playerid]) + " points")

    except ValueError:
        logger.warning("This is not a point: " + str(tweet) + " ("+str(id)+")")

for master,players in scoreboards.iteritems():
    scorefile = open(str(master)+".score", "w")
    for player,points in players.iteritems():
        scorefile.write(str(player)+";"+str(points)+"\n")
    scorefile.close()

date = datetime.date.today()
if date.weekday() == 6:
    for master,players in scoreboards.iteritems():
        tweet = "Placar "+str(date.day)+"/"+str(date.month)+"/"+str(date.year)+" do @" + str(api.get_user(master).screen_name)
        for player,points in players.iteritems():
            tweet = tweet + "\n" + str(api.get_user(player).screen_name) + ": " + points
        print(tweet)
        #api.update_status(tweet)
        logger.info("Tweeted scoreboard of master " + str(api.get_user(master).screen_name))
