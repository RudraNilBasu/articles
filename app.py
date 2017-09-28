from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json

consumer_key=os.getenv('TWITTER_CONSUMER_KEY', 'utf-8')
consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET', 'utf-8')
access_token=os.getenv('TWITTER_ACCESS_TOKEN', 'utf-8')
access_token_secret=os.getenv('TWITTER_ACCESS_SECRET', 'utf-8')

class LikedTweetsListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if 'event' in tweet and tweet['event'] == "favourite":
            print(tweet)
        return True

    def on_error(self, status):
        print("Error status received: {0}".format(status))

if __name__ == '__main__':
    l = LikedTweetsListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.userstream()
