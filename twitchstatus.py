import configvars as cfg
import requests as rq
import json
import time
import tweepy

#Twith auth:
header =  {'Authorization' : cfg.OAUTH_TOKEN, 'Client-ID' : cfg.TWITCH_CLIENT_ID, }

#We'll put our streamers objects in this
streamers = []

#Twitter authorization
auth = tweepy.OAuthHandler(cfg.TWITTER_CONSUMER_KEY, cfg.TWITTER_CONSUMER_SECRET)
auth.set_access_token(cfg.TWITTER_ACCESS_TOKEN, cfg.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Each streamer is a class with a name, url and a live status. Todo: create method to switch status
class Streamer:
    def __init__(self, name, url, streamURL):
        self.name = name
        self.url = url
        self.isLive = False
        self.streamURL = streamURL
        print("Added streamer: " + self.name)

#We'll create our streamers here
# example:
# streamers.append(Streamer('Destiny', "https://api.twitch.tv/helix/streams?user_login=destiny", "https://www.twitch.tv/destiny"))

# Check is a streamer is live. If necessary switch the status of the object
def checkIsLive(s):
    r = rq.get(s.url, headers=header)
    respons = json.loads(r.text)
    if len(respons["data"]) > 0:
        if s.isLive == False:
            s.isLive = True
            tweetStatusChange(s, 1)
    else:
        if s.isLive == True:
            s.isLive = False
            tweetStatusChange(s, 0)

#tweet if a streamer has gone live or went offline
def tweetStatusChange(s, stat):
    if stat == 0:
        status = s.name + " just went offline: " + s.streamURL + " " + time.ctime(time.time())
        api.update_status(status=status)
    if stat == 1:
        status = s.name + " just went online: " + s.streamURL + " " + time.ctime(time.time())
        api.update_status(status=status)

#main loop
while True:
    for s in streamers:
        checkIsLive(s)
        time.sleep(2)
    time.sleep(10)