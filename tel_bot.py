import os
import requests

def bot_msg(message):
    bot_token = os.environ["TELEGRAM_TOKEN"]
    bot_chatID = os.environ["TELEGRAM_CHAT_ID"]
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={message}"
    requests.get(send_text)
