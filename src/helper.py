# Name: helper.py
# Author: Robin Goyal
# Last-Modified: July 25, 2017
# Purpose: Functions to list, insert, and delete subreddits from database
# Note: Still need to perform error and data handling

import setup
import os
import sqlite3
import sys

def database_exists():
    ''' Create database if it doesn't exist '''

    if not(os.path.isfile('subreddits.db')):
        setup.main()

def recreate():
    ''' Recreate database with new set of subreddits'''

    # Remove database file if it exists
    if os.path.isfile('subreddits.db'):
        os.remove('subreddits.db')

    # Recreate database
    setup.main()

def insert():
    ''' Insert new subreddit into database'''

    # Verify database exists
    database_exists()

    # Subreddit and number of posts to insert
    subreddit, posts = input("Enter input as subreddit, num_posts_val: ").split(',')

    # Open connection to database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Try/Except to limit number of posts to 5
    try:
        if int(posts) > 5:
            print("Max number of posts is 5. Limiting to 5!")
            posts = 5
        else:
            posts = int(posts)
    except:
        print("ERROR: Second input value must be of type int!")
        sys.exit(1)

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
    subreddit, posts = input("Enter input as subreddit, updated_num_posts_val: ").split(',')

    # Try/Except to limit number of posts to 5
    try:
        if int(posts) > 5:
            print("Max number of posts is 5. Limiting to 5!")
            posts = 5
        else:
            posts = int(posts)
    except:
        print("ERROR: Second input value must be of type integer")
        sys.exit(1)

    # Open connection to database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Retrieve subreddit from database
    row = c.execute("SELECT * FROM news WHERE subreddits = ?", (subreddit,))

    # Verify that subreddit exists in database
    if len(list(row)) == 0:
        print("ERROR: Subreddit doesn't exist in database!")
        sys.exit(1)

    # Update number of posts in database
    else:
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