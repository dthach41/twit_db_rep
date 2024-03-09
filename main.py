import pandas as pd
import time
from twit_redis import TwitAPI_Redis
from twit_objects import Tweet
import random as rnd


def main():
    api = TwitAPI_Redis('localhost', 6379)
    print("Testing RedisAPI")
    api.r.flushall()

    # # Testing with sample data
    # follows_sample_df = pd.read_csv(r'C:\Users\thach\ds4300\hw1\follows_sample.csv')
    # for index, row in follows_sample_df.iterrows():
    #     user_id = row['USER_ID']
    #     follows_id = row['FOLLOWS_ID']
    #     api.addFollowing(user_id, follows_id)
    #
    # tweets_sample_df = pd.read_csv(r'C:\Users\thach\ds4300\hw1\tweets_sample.csv')
    # for index, row in tweets_sample_df.iterrows():
    #     user_id = row['USER_ID']
    #     tweet_text = row['TWEET_TEXT']
    #     api.postTweet(Tweet(None, user_id, None, tweet_text))
    #
    # tl_2 = api.getTimeline(2)
    # for tweet in tl_2:
    #     print(tweet.tweet_id, tweet.tweet_text, tweet.tweet_ts)



    # Testing with real data
    follow_df = pd.read_csv(r'../hw1_data/follows.csv')
    for index, row in follow_df.iterrows():
        user_id = row['USER_ID']
        follows_id = row['FOLLOWS_ID']
        api.addFollowing(int(user_id), int(follows_id))


    tweet_df = pd.read_csv(r'../hw1_data/tweet.csv')
    # Inserts each tweet from tweet.csv into tweet table
    postTweet_calls = 0
    duration1 = 5  # Set the duration in seconds
    start_time = time.time()
    tweet_rows = tweet_df.iterrows()
    while time.time() - start_time < duration1:
        try:
            index, row = next(tweet_rows)
            user_id = row['USER_ID']
            tweet_text = row['TWEET_TEXT']
            api.postTweet(Tweet(None, user_id, None, tweet_text))
            postTweet_calls += 1
            print(f"postTweet call {postTweet_calls}: Elapsed time = {time.time() - start_time:.6f} seconds")

        except StopIteration:
            break


    calls = 0
    duration = 5  # Set the duration in seconds
    start_time = time.time()
    # Keep running for 5 seconds
    while time.time() - start_time < duration:
        rand_user_id = rnd.randint(1, 9999)
        api.getTimeline(rand_user_id)
        calls += 1
        print(f"API call {calls}: Elapsed time = {time.time() - start_time:.6f} seconds")

    print('\n', postTweet_calls / duration1, " postTweet calls per second")
    print('\n', calls / duration, " getTimeline calls per second")


if __name__ == '__main__':
    main()