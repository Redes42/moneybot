from typing import Optional

from bot import bot
from telebot.apihelper import ApiTelegramException
from requests.exceptions import ConnectTimeout, ReadTimeout, Timeout
from telebot.types import InlineKeyboardMarkup


def send_safe_message(
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str | None = "HTML",
    image_id: Optional[str] = None
):
    params = dict(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )
    if image_id:
        del params['text']
        params.update(dict(caption=text))
    try:
        if not image_id:
            return bot.send_message(**params)
        else:
            with open('assets/help.jpg', 'rb') as image:
                return bot.send_photo(**params, photo=image)

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
            f'Не удалось отправить сообщение в Telegram\n {message}',
            reply_markup=None,
            parse_mode=None,
        )
