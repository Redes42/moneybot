import logging

import telebot.apihelper
from telebot import types

from bot import bot
from constants import CB_DELIMETER
from menu import MENU, InputStage
from party import parties
from stages import Stages
from flow_manager import manager


@bot.message_handler(commands=[Stages.START])
def start(message: types.Message):
    manager.process(message, Stages.START)
    # MENU[Stages.START].process(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id, '')
    stage = call.data
    if stage in MENU:
        manager.process(call.message, stage)
    else:
        stage, param = call.data.split(CB_DELIMETER)
        manager.process(call.message, stage, int(param))


@bot.message_handler()
def input_data(message: types.Message):
    chat_id = message.chat.id
    if chat_id in parties:
        manager.process(message, parties[chat_id].stage, got_input=True)
    else:
        manager.process(message, Stages.START)


def main():
    try:
        bot.polling(interval=1)
    except telebot.apihelper.ApiTelegramException as error:
        print(error)
    except telebot.apihelper.ApiHTTPException as error:
        print(error)
    except telebot.apihelper.ApiInvalidJSONException as error:
        print(error)


if __name__ == '__main__':
    main()