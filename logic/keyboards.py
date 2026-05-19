from decimal import Decimal
from typing import Callable

from telebot import types

from flow.callback_codec import CallbackCodec
from flow.stage_data import StageData

type KeyboardBuilder = Callable[['SelectStage', StageData], types.InlineKeyboardMarkup | None]

def build_back_button(stage: 'SelectStage') -> types.InlineKeyboardButton:
    return  types.InlineKeyboardButton(
        text='< Назад',
        callback_data=CallbackCodec.encode_stage(stage.parent)
    )


def build_children_keyboard(stage: 'SelectStage', data: StageData) -> types.InlineKeyboardMarkup | None:
    keyboard = types.InlineKeyboardMarkup()
    if stage.children:
        for child in stage.children:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=child.button_caption,
                    callback_data=CallbackCodec.encode_stage(child),
                )
            )
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard

def build_add_participant_keyboard(stage: "SelectStage", data: StageData)-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    participant_ids = tuple(
        participant.person_id for participant in data.party.participants
    )
    for person in data.people:
        if person.id not in participant_ids:
            participant = {'participant_id': person.id}
            button_left = types.InlineKeyboardButton(
                text=person.with_coeff(),
                callback_data=CallbackCodec.encode_payload(
                    {
                        **participant,
                        'coeff': person.coeff
                    }
                )
            )
            button_right = types.InlineKeyboardButton(
                person.without_coeff(),
                callback_data=CallbackCodec.encode_payload(participant)
            )
            keyboard.add(button_left, button_right)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard

def build_remove_participant_keyboard(stage: 'SelectStage', data: StageData)-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for participant in data.party.participants:
        participant_data = {'participant_id': participant.person_id}
        button = types.InlineKeyboardButton(
            text=participant.with_coeff_and_payment(),
            callback_data=CallbackCodec.encode_payload(
                participant_data
            )
        )
        keyboard.add(button)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard


def build_remove_person_keyboard(stage: 'SelectStage', data: StageData)-> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for person in data.people:
        person_data = {'person_id': person.id}
        button = types.InlineKeyboardButton(
            text=person.with_coeff(),
            callback_data=CallbackCodec.encode_payload(person_data)
        )
        keyboard.add(button)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard