import os
import telebot

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"), parse_mode=None)


def bot_msg(message: str):
    bot.send_message(os.getenv('TELEGRAM_CHAT_ID'), message)
