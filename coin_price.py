import requests as r
import logging
import re
from tel_bot import bot_msg
from fb import get_pct_from_fb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_current_price(coin: str) -> float:
    url = f"https://api.coinranking.com/v1/public/coins?symbols={coin}"
    current_price = float(r.get(url=url).json()["data"]["coins"][0]["price"])
    return round(current_price, no_of_decimals(current_price))


def no_of_decimals(price: float) -> int:
    return 2 if price > 1 else 5


def predict_price(account, from_tweet) -> None:
    '''
        Prediction % will be retrieved from
        firebase and added to the current price.
        Subject to a dynamic change.
    '''

    if from_tweet.text[0:2] == 'RT':
        return

    if not from_tweet.favorited:
        try:
            from_tweet.favorite()
        except Exception as e:
            logger.error("Error on fav")

    if not from_tweet.retweeted:
        try:
            from_tweet.retweet()
        except Exception as e:
            logger.error("Error on retweet")

    coin_from_tweet = find_coin(from_tweet.text)
    current_coin_price = get_current_price(coin_from_tweet)
    predicted_price = round(
        current_coin_price + current_coin_price * get_pct_from_fb(), no_of_decimals(current_coin_price))
    try:
        account.api.update_status(
            f"${predicted_price}", in_reply_to_status_id=from_tweet.id, auto_populate_reply_metadata=True)
        bot_msg(f"PP: Current {coin_from_tweet} price: ${current_coin_price}")
        bot_msg(f"PP: You guessed the price of ${predicted_price}!")
    except Exception as e:
        logger.error("Error on commenting the price")
        bot_msg(f"Failed to retweet with comment!")


def find_coin(from_text: str):
    return re.search('(\$[A-Z])\w+', from_text).group()[1:]
