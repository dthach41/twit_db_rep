import datetime as date


class Tweet:

    def __init__(self, tweet_id, user_id, tweet_ts, tweet_text):
        self.tweet_id = tweet_id
        self.user_id = user_id
        if tweet_ts is not None:
            self.tweet_ts = tweet_ts
        else:
            self.tweet_ts = tweet_ts.strftime('%Y-%m-%d') if tweet_ts else None

        self.tweet_text = tweet_text


    def __str__(self):
        return (f'Tweet ID: {self.tweet_id}, User ID: {self.user_id},'
                f' Timestamp: {self.tweet_ts}, Text: {self.tweet_text}')





class Followings:
    def __init__(self, user_id, follows_id):
        self.user_id = user_id
        self.follows_id = follows_id

    def __str__(self):
        return f'User ID: {self.user_id}, Follows ID: {self.follows_id}'

