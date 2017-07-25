# Name: setup.py
# Author: Robin Goyal
# Last-Modified: July 25, 2017
# Purpose: Perform a setup for the subreddits database from a csv file
# Note: Setup file is only meant to be run once and csv file should have
#       format similar to example.csv. Currently, no checks are made for
#       improper formats

import sqlite3
import sys
import os

def main():

    # Get raw subreddits from csv files
    raw_subreddits = read_csv()

    # Clean up data from csv file
    cleaned_subreddits = cleanup(raw_subreddits)

    # Move cleaned data to database and remove csv file
    create_database(cleaned_subreddits)
    os.remove('subreddits.csv')

def cleanup(raw_data):
    
    # Remove newline characters and split at comma
    cleaned_data = [row.strip('\n').split(',') for row in raw_data]

    # Convert the number of posts field to integer value
    for i in range(len(cleaned_data)):

        #
        try:
            if int(cleaned_data[i][1]) > 5:
                print("Max number of posts is 5. Limiting to 5!")
                cleaned_data[i][1] = 5
            else:
                cleaned_data[i][1] = int(cleaned_data[i][1])
        except:
            print("ERROR: The 2nd value in the csv value must be an integer value")
            sys.exit(1)

    return cleaned_data


def create_database(clean_data):

    # Check if database doesn't exist.
    if os.path.isfile('subreddits.db'):
        print("ERROR: Database already exists. Use Python helper functions to recreate database or other functions.")
        sys.exit(1)

    # Open or create database and use cursor to execute SQL commands
    conn = sqlite3.connect('subreddits.db')
    c = conn.cursor()

    # Create table
    c.execute(''' CREATE TABLE news
                (subreddits text, posts integer)''')

    # Insert data
    for i in clean_data:
        element = (i[0], i[1])
        c.execute('INSERT INTO news VALUES (?, ?)', element)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def read_csv():

    # Open csv file containing favourite subreddits
    try: 
        f = open('subreddits.csv', 'r')
    except:
        print("ERROR: Create a subreddits.csv file with your favourite subreddits and number of posts!")
        sys.exit(1)

    # Read subreddits from CSV file
    data = f.readlines()

    # Close file
    f.close()

    # Return subreddits
    return data

if __name__ == "__main__":
    main()