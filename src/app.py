import praw
from twilio.rest import Client
import requests
import json
import os
import sqlite3

def get_posts(subreddits):
    client_id = os.environ.get('REDDIT_CLIENT_ID')
    secret_id = os.environ.get('REDDIT_SECRET_ID')
    user_agent = os.environ.get('REDDIT_USER_AGENT')

    reddit = praw.Reddit(client_id = client_id, client_secret = secret_id,
                         user_agent = user_agent)

    for subreddit in subreddits:
        submissions = list(reddit.subreddit(subreddit[0]).hot(limit = subreddit[1]))
        print("SUBREDDIT: %s\n" % subreddit[0])
        for i in submissions:
            print('{:.30}: {}\n'.format(i.title, i.url))


def shorten_url(url):
    API_KEY = os.environ.get('GOOGLE_API_KEY')
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=%s' % (API_KEY)
    payload = json.dumps({'longUrl': url})
    headers = {'Content-Type': 'application/json'}
    r = requests.post(post_url, data=payload, headers=headers)
    return r.json()['id']

get_posts([['learnpython', 5], ['learnprogramming', 2]])

#print(shorten_url('https://stackoverflow.com/questions/17357351/how-to-use-google-shortener-api-with-python'))