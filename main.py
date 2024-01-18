# Imports
import os
import pandas as pd
import random as rnd
import time
from twit_mysql import TwitAPI
from twit_objects import Tweet, Followings

def main():

    # Authenticate
    api = TwitAPI(os.environ['TWIT_USER'], os.environ['TWIT_PASSWORD'], os.environ['TWIT_DATABASE'])

    # Uncomment to delete all rows in tweet table and followings table
    # api.clearTweets()
    # api.clearFollowings()

    """
    Testing with the sample data
    """
    # follows_sample_df = pd.read_csv(r'C:\Users\thach\ds4300\hw1\follows_sample.csv')
    # for index, row in follows_sample_df.iterrows():
    #     user_id = row['USER_ID']
    #     follows_id = row['FOLLOWS_ID']
    #     api.addFollowing(int(user_id), int(follows_id))
    #
    #
    #
    # tweets_sample_df = pd.read_csv(r'C:\Users\thach\ds4300\hw1\tweets_sample.csv')
    # for index, row in tweets_sample_df.iterrows():
    #     user_id = row['USER_ID']
    #     tweet_text = row['TWEET_TEXT']
    #     api.postTweet(Tweet(None, user_id, None, tweet_text))

    # followings_df = api.getFollowings()
    # tweet_df = api.getTweets()

    # for i in range(1, 6):
    #     print('User_ID:', i)
    #     api.getTimeline(i)


    """
    Performance testing with the actual test data
    """
    #
    # follow_df = pd.read_csv(r'hw1_data\follows.csv')
    # for index, row in follow_df.iterrows():
    #     user_id = row['USER_ID']
    #     follows_id = row['FOLLOWS_ID']
    #     api.addFollowing(int(user_id), int(follows_id))



    tweet_df = pd.read_csv(r'hw1_data\tweet.csv')
    # Inserts each tweet from tweet.csv into tweet table
    # Run with profiler to get total time in ms and / by 1 million
    for index, row in tweet_df.iterrows():
        user_id = row['USER_ID']
        tweet_text = row['TWEET_TEXT']
        api.postTweet(Tweet(None, user_id, None, tweet_text))



    # Gets a random users timeline
    calls = 0
    duration = 5  # Set the duration in seconds
    start_time = time.time()
    # Keep running for 5 seconds
    while time.time() - start_time < duration:
        rand_user_id = rnd.randint(1, 5000)
        print('User ID: ', rand_user_id)
        api.getTimeline(rand_user_id)
        calls += 1
        #print(f"API call {calls}: Elapsed time = {time.time() - start_time:.6f} seconds")

    print('\n', calls / duration, " getTimeline calls per second")



if __name__ == '__main__':
    main()
