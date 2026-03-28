from constants import CB_DELIMETER
from stages import Stages
from person import Person
from telebot import types


def create_participants_keyboard(participants: list[Person])-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for participant in participants:
        button_left = types.InlineKeyboardButton(
            participant.with_coeff(),
            callback_data=f'{Stages.DEFINE_PAYMENT}{CB_DELIMETER}{participant.id}'
        )
        button_right = types.InlineKeyboardButton(
            participant.without_coeff(),
            callback_data=f'{Stages.DEFINE_COEFF}{CB_DELIMETER}{participant.id}'
        )
        keyboard.add(button_left, button_right)
    button = types.InlineKeyboardButton(
        '< Назад',
        callback_data=Stages.NEW_PARTY
    )
    keyboard.add(button)
    return keyboard