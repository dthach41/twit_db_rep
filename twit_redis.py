"""
Represents redis api
- set a counter for tweet_id
- create a sorted set timeline for each user
- use a set for list of followers and followings of each user
- used hashmap to hold data about each tweet
"""

import redis
from twit_objects import Tweet

class TwitAPI_Redis:
    def __init__(self, host, port):
        self.r = redis.Redis(host, port, decode_responses=True)
        self.r.set('tweet_counter', 0)


    # Adds a new following to Followings set of user_id
    # also adds a new follower to Followers of follows_id
    def addFollowing(self, user_id, follows_id):
        self.r.sadd('followings' + str(user_id), str(follows_id))
        self.r.sadd('followers' + str(follows_id), str(user_id))



    # Insert a new tweet into the redis db, and update timelines for user of new tweet
    def postTweet(self, new_tweet: Tweet):
        self.r.incr('tweet_counter')
        tweet_id = self.r.get('tweet_counter')
        new_tweet.tweet_id = tweet_id
        new_tweet.tweet_ts = self.r.time()[1]

        self.r.hset('tweet:' + tweet_id, mapping={'tweet_id': tweet_id,
                                                   'user_id': new_tweet.user_id,
                                                   'tweet_ts': new_tweet.tweet_ts,
                                                   'tweet_text': new_tweet.tweet_text})

        self.updateTimeline(new_tweet.user_id, new_tweet)


    # Updates the timelines for all of user_id's followers
    def updateTimeline(self, user_id, new_tweet: Tweet):
        user_followers = self.r.smembers('followers' + str(user_id))

        for follower_id in user_followers:
            # Uses the tweet's timestamp as the score in sorted set
            self.r.zadd('timeline' + str(follower_id), {str(new_tweet.tweet_id) : new_tweet.tweet_ts})


    # Gets list of most recent 10 tweets on user_id's timeline
    def getTimeline(self, user_id):
        # Reverse so that latest/newest tweets appear at the top
        tl_tweets = self.r.zrevrange('timeline' + str(user_id), 0, 9, withscores=True)
        timeline = []
        for i in range(0, len(tl_tweets)):
            id = str(tl_tweets[i][0])
            tweet_obj = Tweet(self.r.hget('tweet:' + id, 'tweet_id'),
                              self.r.hget('tweet:' + id, 'user_id'),
                              self.r.hget('tweet:' + id, 'tweet_ts'),
                              self.r.hget('tweet:' + id, 'tweet_text'))
            timeline.append(tweet_obj)

        return timeline





