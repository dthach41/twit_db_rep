"""
Represents redis api

- representing tweet characteristics in a list, assigned an ID
- put ID into a set for efficient searching
"""

import redis
from twit_objects import Tweet

class TwitAPI_Redis:
    def __init__(self, host, port):
        self.r = redis.Redis(host, port, decode_responses=True)

    # Insert a new tweet into the redis db
    def postTweet(self, new_tweet: Tweet):
        self.r.lpush()



def main():
    api = TwitAPI_Redis('localhost', 6379)
    print("Testing RedisAPi")
    api.r.flushall()





if __name__ == '__main__':
    main()





