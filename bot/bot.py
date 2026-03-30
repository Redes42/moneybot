import os

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from requests.exceptions import ConnectTimeout, ReadTimeout, Timeout
from telebot.types import InlineKeyboardMarkup



load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)

def send_safe_message(
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str | None = "HTML",
):
    try:
        return bot.send_message(
            chat_id,
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )

    except (Timeout, ReadTimeout, ConnectTimeout):
        return bot.send_message(
            chat_id,
            "Сетевой таймаут. Попробуйте ещё раз.",
            reply_markup=None,
            parse_mode=None,
        )

    except ApiTelegramException as exc:
        message = str(exc).lower()

        if "can't parse entities" in message or "parse entities" in message:
            return bot.send_message(
                chat_id,
                text,
                reply_markup=reply_markup,
                parse_mode=None,
            )

        if "message is too long" in message:
            short_text = str(text)[:4000]
            return bot.send_message(
                chat_id,
                short_text,
                reply_markup=reply_markup,
                parse_mode=None,
            )

        return bot.send_message(
            chat_id,
            "Не удалось отправить сообщение в Telegram.",
            reply_markup=None,
            parse_mode=None,
        )
