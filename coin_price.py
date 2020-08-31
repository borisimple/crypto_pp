import requests as r
from tel_bot import bot_msg


def get_current_price(coin):
    url = f"https://api.coinranking.com/v1/public/coins?symbols={coin}"
    current_price = float(r.get(url=url).json()["data"]["coins"][0]["price"])
    return round(current_price, no_of_decimals(current_price))


def no_of_decimals(price):
    return 2 if price > 1 else 5


def predict_price(account, from_tweet):
    '''
        "Prediction" will be a static +10% on the current price.
        Subject to a dynamic change.
    '''
    if from_tweet.text[0:2] == 'RT':
        return "Skipping retweet"

    tweet_url = f"https://twitter.com/{from_tweet.user.screen_name}/status/{from_tweet.id}"
    coin_from_tweet = account.find_coin(from_tweet.text)
    current_coin_price = get_current_price(coin_from_tweet)
    predicted_price = round(
        current_coin_price + current_coin_price * 0.1, no_of_decimals(current_coin_price))
    try:
        account.api.update_status(f"${predicted_price} {tweet_url}")
    except:
        bot_msg(f"Failed to retweet with comment!")

    bot_msg(f"PP: Current {coin_from_tweet} price: ${current_coin_price}")
    bot_msg(f"PP: You guessed the price of ${predicted_price}!")
