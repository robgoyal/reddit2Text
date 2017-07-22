# Name: helper.py
# Author: Robin Goyal
# Last-Modified: July 22, 2017
# Purpose: Functions to list, insert, and delete subreddits from database
# Note: At the moment, the assumption is that the user correctly inputs data

import setup
import os
import sqlite3


def database_exists():
    if not(os.path.isfile('subreddits.db')):
        setup.main()

def insert():

    database_exists()

    subreddit, posts = input("Enter subreddit and number of posts: ").split(',')

    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    c.execute("INSERT INTO news VALUES (?, ?)",(subreddit, int(posts)))

    conn.commit()
    conn.close()

def list_subreddits():
    
    database_exists()

    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    rows = list(c.execute("SELECT * FROM news"))

    for i in rows: print("%s, %d" % (i[0], i[1]))

    conn.close()

def delete():
    pass