import praw
from twilio.rest import Client
import requests
import json
import os

def shorten_url(url):
    API_KEY = os.environ.get('GOOGLE_API_KEY')
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=%s' % (API_KEY)
    payload = json.dumps({'longUrl': url})
    headers = {'Content-Type': 'application/json'}
    r = requests.post(post_url, data=payload, headers=headers)
    return r.json()['id']

print(shorten_url('https://stackoverflow.com/questions/17357351/how-to-use-google-shortener-api-with-python'))