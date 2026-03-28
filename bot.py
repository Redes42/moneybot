import os

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)