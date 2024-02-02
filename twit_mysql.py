import pandas as pd

from dbutils import DBUtils
from twit_objects import Tweet, Followings

class TwitAPI:
    def __init__(self, user, password, database, host='localhost'):
        self.dbu = DBUtils(user, password, database, host)

    def closeConnection(self):
        self.dbu.close()

    # Gets tweet table
    def getTweets(self) -> pd.DataFrame:
        sql = ("SELECT * FROM tweet;")
        df = self.dbu.execute(sql)
        result = [Tweet(*df.iloc[i][0:]) for i in range(len(df))]
        print(df)
        return result

    # Adds new tweet to Tweet table
    def postTweet(self, new_tweet: Tweet):
        sql = ("INSERT INTO tweet (tweet_id, user_id, tweet_ts, tweet_text)"
                " VALUES (%s, %s, %s, %s)")
        val = (new_tweet.tweet_id, new_tweet.user_id, new_tweet.tweet_ts, new_tweet.tweet_text)
        self.dbu.insert_one(sql, val)


    # Clears the tweet table
    def clearTweets(self):
        sql = ("DELETE FROM tweet;")
        self.dbu.execute(sql)
        sql = ("ALTER TABLE tweet AUTO_INCREMENT = 1;")
        self.dbu.execute(sql)

    # Gets the followings table
    def getFollowings(self):
        sql = ("SELECT * FROM followings")
        df = self.dbu.execute(sql)
        result = [Followings(*df.iloc[i][0:]) for i in range(len(df))]
        print(df)
        return result

    # Add new following to followings table
    def addFollowing(self, user_id, following_id):
        sql = ("INSERT INTO followings (user_id, follows_id) VALUES (%s, %s)")
        val = (user_id, following_id)
        self.dbu.insert_one(sql, val)

    # Gets the most recent tweets in given user's timeline
    def getTimeline(self, user_id):
        sql = ("SELECT t.tweet_id, t.user_id, t.tweet_ts, t.tweet_text "
               "FROM tweet t "
               "LEFT JOIN followings f ON (f.follows_id = t.user_id) "
               "WHERE f.user_id =" + str(user_id) + " " +
               "ORDER BY f.user_id "
               "LIMIT 10;")

        df = self.dbu.execute(sql)
        timeline = [Tweet(*df.iloc[i][0:]) for i in range(len(df))]
        return timeline

    # Clears the followings table
    def clearFollowings(self):
        sql = ("DELETE FROM followings;")
        self.dbu.execute(sql)



