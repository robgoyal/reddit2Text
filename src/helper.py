# Name: helper.py
# Author: Robin Goyal
# Last-Modified: July 23, 2017
# Purpose: Functions to list, insert, and delete subreddits from database
# Note: Still need to perform error and data handling

import setup
import os
import sqlite3

def database_exists():
    ''' Create database if it doesn't exist '''

    if not(os.path.isfile('subreddits.db')):
        setup.main()

def insert():
    ''' Insert new subreddit into database'''

    # Verify database exists
    database_exists()

    # Subreddit and number of posts to insert
    subreddit, posts = input("Enter subreddit and number of posts: ").split(',')

    # Open connection to database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    c.execute("INSERT INTO news VALUES (?, ?)",(subreddit, int(posts)))

    # Commit changes and close connection
    conn.commit()
    conn.close()

def list_subreddits():
    ''' List all subreddits in database'''

    # Verify database exists
    database_exists()

    # Open connection to database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # List each subreddit with number of posts
    rows = list(c.execute("SELECT * FROM news"))
    for i in rows: print("%s, %d" % (i[0], i[1]))

    # Close connection
    conn.close()

def update_posts():
    ''' Update the number of posts for a subreddit'''

    # Verify database exists
    database_exists()

    # Subreddit and number of posts to update
    subreddit, posts = input("Enter subreddit and updated posts: ").split(',')

    # Limit number of posts to 5
    if int(posts) > 5:
        posts = 5
    else:
        posts = int(posts)

    # Open connection to database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Update number of posts in database
    c.execute("UPDATE news SET posts = ? WHERE subreddits = ?", (posts, subreddit))

    # Commit changes and close connection
    conn.commit()
    conn.close()

def delete():
    
    # Verify database exists
    database_exists()

    # Subreddit to delete
    subreddit = input("Enter subreddit to delete: ")

    # Open connection to database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Delete subreddit from database
    c.execute("DELETE FROM news WHERE subreddits = ?", (subreddit,))

    # Commit changes and close connection
    conn.commit()
    conn.close()