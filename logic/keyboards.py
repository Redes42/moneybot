from typing import Callable

from telebot import types

from bot.callback_codec import CallbackCodec
from flow.stage_data import StageData

type KeyboardBuilder = Callable[['SelectStage', StageData], types.InlineKeyboardMarkup | None]

def build_children_keyboard(stage: "SelectStage", data: StageData) -> types.InlineKeyboardMarkup | None:
    keyboard = types.InlineKeyboardMarkup()
    for child in stage.children:
        keyboard.add(
            types.InlineKeyboardButton(
                text=child.title,
                callback_data=CallbackCodec.encode_stage(child),
            )
        )
    if stage.parent:
        keyboard.add(
            types.InlineKeyboardButton(
                text='< Назад',
                callback_data=CallbackCodec.encode_stage(stage.parent),
            )
        )
    return keyboard

def build_add_participant_keyboard(stage: "SelectStage", data: StageData)-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for person in data.people:
        person_id = {'participant_id': person.id}
        button_left = types.InlineKeyboardButton(
            text=person.with_coeff(),
            callback_data=str(
                {
                    **person_id,
                    'coeff': person.coeff
                }
            )
        )
        button_right = types.InlineKeyboardButton(
            person.without_coeff(),
            callback_data=str(person_id)
        )
        keyboard.add(button_left, button_right)
    button = types.InlineKeyboardButton(
        '< Назад',
        callback_data=stage.name
    )
    keyboard.add(button)
    return keyboard

def build_remove_participants_keyboard(stage: "SelectStage", data: StageData)-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for participant in data.party.participants:
        button_left = types.InlineKeyboardButton(
            participant.with_coeff(),
            callback_data='' # f'{Stages.DEFINE_PAYMENT}::{participant.person_id}'
        )
        button_right = types.InlineKeyboardButton(
            participant.without_coeff(),
            callback_data='' # f'{Stages.DEFINE_COEFF}::{participant.person_id}'
        )
        keyboard.add(button_left, button_right)
    button = types.InlineKeyboardButton(
        '< Назад',
        callback_data=Stages.NEW_PARTY
    )
    keyboard.add(button)
    return keyboard