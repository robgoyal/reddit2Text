# Name: setup.py
# Author: Robin Goyal
# Last-Modified: July 22, 2017
# Purpose: Perform a setup for the subreddits database from a csv file
# Note: Setup file is only meant to be run once and csv file should have
#       format similar to example.csv. Currently, no checks are made for
#       improper formats

import sqlite3
import sys
import os

def main():

    # Get raw subreddits from csv files
    raw_subreddits = read_subreddits()

    # Clean up data from csv file
    cleaned_subreddits = cleanup(raw_subreddits)

    # Move cleaned data to database and remove csv file
    create_database(cleaned_subreddits)
    os.remove('subreddits.csv')

def cleanup(data):
    
    # Remove newline charactesr and split at comma
    cleaned_data = [row.strip('\n').split(',') for row in data]

    # Convert number of posts to int
    for i in range(len(cleaned_data)):

        # Limit number of posts to 5
        if int(cleaned_data[i][1]) > 5:
            cleaned_data[i][1] = 5
        else:
            cleaned_data[i][1] = int(cleaned_data[i][1])

    return cleaned_data


def create_database(data):

    # Open or create database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Create table
    c.execute(''' CREATE TABLE news
                (subreddits text, posts integer)''')

    # Insert data
    for i in data:
        element = (i[0], i[1])
        c.execute('INSERT INTO news VALUES (?, ?)', element)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def read_subreddits():

    # Open csv file containing favourite subreddits
    try: 
        f = open('subreddits.csv', 'r')
    except:
        print("ERROR: Create a subreddits.csv file with your favourite subreddits!")
        sys.exit(1)

    # Read subreddits from CSV file
    rows = f.readlines()

    # Close file
    f.close()

    # Return subreddits
    return rows

if __name__ == "__main__":
    main()