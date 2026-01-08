import logging
import os


from dotenv import load_dotenv
import telebot
from telebot import TeleBot


load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def main():
    bot = TeleBot(token=TELEGRAM_TOKEN)
    bot.polling(interval=1)

if __name__ == '__main__':
    main()