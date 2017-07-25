# Reddit 2 Text

## Motivation

The motivation for this project came from an attempt to reduce wasted time spent on social media sites and reddit. This script would take top daily posts from my favourite subreddits and send the links through text. 

![Example of Text](https://github.com/robgoyal/reddit2Text/img/example.png "Example Text")

## Procedure

This project has been greatly exaggerated in complexity but that gave me an opportunity to learn more through the various API's and Python modules.

Some of the challenges involved were using an sqlite database and parsing basic data from a csv file. Communicating with the Reddit API and Google URL shortener API required spending a lot of time reading documentation. The final challenge was determining how to secure the API ID's and KEY's from the scripts while simultaneously enabling them to be a part of a cron task.

## Setup

The core requirements for this task is to get a Reddit API Client and Secret ID, Google URL shortener API Key, and a TWILIO Client and Secret ID. This 

The only input required is a subreddit.csv file with your favourite subreddits and the number of posts wanted for each subreddit. 

Initial setup command:

```
python setup.py
```

There are multiple helper functions in the helper.py file. You can run these functions from the command line. You can recreate the database with a subreddit.csv file, insert a new subreddit, delete a subreddit, update the posts for a subreddit, and list the subreddits there.

```
python -c "import helper; helper.list_subreddits()"
python -c "import helper; helper.recreate()"
```

The core logic is in app.py which you can run from the command line as well. This could be set as a cron task so that each day at a certain time, you get the posts on the go wherever you are.
