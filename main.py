import os
import tweepy
from tel_bot import bot_msg
from coin_price import predict_price


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        predict_price(self, tweet)

    def on_error(self, status):
        bot_msg(f"PP failed because of status: {status}")
        return False


def main():
    auth = tweepy.OAuthHandler(
        os.getenv('TW_API_KEY'), os.getenv('TW_API_KEY_SECRET'))

    auth.set_access_token(os.getenv('TW_ACCESS_TOKEN'),
                          os.getenv('TW_ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    contest_listener = MyStreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=contest_listener)
    stream.filter(follow=['1299989040700297216'])
    stream.filter(track=["Predict and win"])


if __name__ == "__main__":
    main()
