import os
import tweepy
from tel_bot import bot_msg
from coin_price import predict_price, logger


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):

        if not correct_tweet(self, tweet):
            return
        predict_price(self, tweet)

    def on_error(self, status):
        logger.error(status)
        bot_msg(f"PP failed because of status: {status}")
        return False


def correct_tweet(account, tweet_text):
    if tweet_text.in_reply_to_status_id is not None \
            or tweet_text.in_reply_to_user_id is not None \
            or tweet_text.is_quote_status is True \
            or tweet_text.user.id_str != os.getenv('ACC_ID') \
            or tweet_text.user.id == account.me.id \
            or not tweet_text.text.startswith('Predict and win'):
        return False

    return True


def main():
    auth = tweepy.OAuthHandler(
        os.getenv('TW_API_KEY'), os.getenv('TW_API_KEY_SECRET'))

    auth.set_access_token(os.getenv('TW_ACCESS_TOKEN'),
                          os.getenv('TW_ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    contest_listener = MyStreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=contest_listener)
    stream.filter(follow=[os.getenv('ACC_ID')])
    stream.filter(track=["Predict and win"], languages=["en"])


if __name__ == "__main__":
    main()
