import praw
from twilio.rest import Client
import requests
import json
import os
import sqlite3
import setup

def main():

    # Create database if file doesn't exist
    if not(os.path.isfile('subreddits.db')):
        setup.main()

    # Open connection to database
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Retrieve subreddits from database
    rows = list(c.execute("SELECT * FROM news"))
    print(rows)

    # Close connection
    conn.close()

    # Grab posts for each subreddit
    posts = get_posts(rows)

    # Create text for posts
    print(compose_message(posts))


def compose_message(dict_posts):

    # Retrieve environment variables for TWILIO client
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    # Initialize twilio client
    client = Client(account_sid, auth_token)

    # Text message format specified
    text = ""
    post_format = '-{:.50}: {}\n'

    # Prepare text message with subreddit name with top post titles and links
    for post in dict_posts.keys():
        text += '{}\n'.format(post.upper())
        subreddit_posts = dict_posts[post]

        for sub_post in subreddit_posts:
            text += post_format.format(sub_post.title, shorten_url(sub_post.url))   

        text += '\n'
    
    # Send text with prepared message
    # To and From must be authorized with Twilio account
    message = client.messages.create(to="+12894892495",
                                     from_="+12892051305",
                                     body=text)

    return message.sid

def get_posts(subreddits):

    # Retrieve environment variables for REDDIT client
    client_id = os.environ.get('REDDIT_CLIENT_ID')
    secret_id = os.environ.get('REDDIT_SECRET_ID')
    user_agent = os.environ.get('REDDIT_USER_AGENT')

    # Initialize reddit instance
    reddit = praw.Reddit(client_id = client_id, client_secret = secret_id,
                         user_agent = user_agent)

    # Prepare dictionary of subreddit and submissions
    posts = {}
    for subreddit in subreddits:

        # Retrieve top submissions for subreddit if it exists
        try:
            submissions = list(reddit.subreddit(subreddit[0]).top(limit = subreddit[1]))
        except:
            print('ERROR: The subreddit, {} doesn\'t exist. Delete using helper function.\n'.format(subreddit[0]))

        # Set value of subreddit key to list of submissions
        posts[subreddit[0]] = submissions

    return posts

def shorten_url(url):

    # Retrieve API KEY for URL shortener API
    API_KEY = os.environ.get('GOOGLE_API_KEY')

    # Setup request for payload
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=%s' % (API_KEY)
    payload = json.dumps({'longUrl': url})
    headers = {'Content-Type': 'application/json'}

    # Request and return short url
    r = requests.post(post_url, data=payload, headers=headers)
    return r.json()['id']

if __name__=='__main__':
    main()