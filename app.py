from __future__ import absolute_import, print_function
from __future__ import unicode_literals
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
from flask import Flask, render_template

consumer_key=os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET')
access_token=os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html", articles=sorted(articles, key=lambda article: article["liked_on"], reverse=True))

articles = []

class LikedTweetsListener(StreamListener):
    def on_data(self, data):
        story_url = 'https://t.co/gAmeEaTw8U'
        if story_url:
            article = extract_article(story_url)
            if article:
                article['story_url'] = story_url
                article['liked_on'] = 20#time.time()
                articles.append(article)
                print("DONE")
        tweet = json.loads(data)
        print(tweet['event'])
        if 'event' in tweet and tweet['event'] == "favourite":
            liked_tweet = tweet["target_object"]
            liked_tweet_text = liked_tweet["text"]
            story_url = extract_url(liked_tweet)
            if story_url:
                article = extract_article(story_url)
                if article:
                    article['story_url'] = story_url
                    article['liked_on'] = time.time()
                    articles.append(article)
        return True

    def on_error(self, status):
        print("Error status received: {0}".format(status))

def extract_url(liked_tweet):
    url_entities = liked_tweet["entities"]["urls"]
    if url_entities and len(url_entities) > 0:
        return url_entities[0]['expanded_url']
    else:
        return None

from newspaper import Article

def extract_article(story_url):
    article = Article(story_url)
    article.download()
    article.parse()
    title = article.title
    img = article.top_image
    publish_date = article.publish_date
    text = article.text.split('\n\n')[0] if article.text else ""
    return {
            'title':title,
            'img':img,
            'publish_date':publish_date,
            'text':text.encode('ascii','ignore')
    }

if __name__ == '__main__':
    l = LikedTweetsListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #print(os.getenv('TWITTER_CONSUMER_KEY'))

    stream = Stream(auth, l)
    stream.userstream(async=True)
    app.run(debug=True)
