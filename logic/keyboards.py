from dataclasses import dataclass
from decimal import Decimal
from typing import Callable

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.app import Users
from flow.callback_codec import CallbackCodec
from flow.stage_data import StageData

type KeyboardBuilder = Callable[['SelectStage', StageData], InlineKeyboardMarkup]


@dataclass
class Choice:
    key: str
    text: str


def build_back_button(stage: 'SelectStage') -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text='< Назад',
        callback_data=CallbackCodec.encode_stage(stage.parent)
    )

def build_choices_keyboard(stage: 'SelectStage', data: StageData) ->  InlineKeyboardMarkup | None:
    keyboard = InlineKeyboardMarkup()
    choices = data.payload.get('choices')
    if choices:
        for choice in choices:
            keyboard.add(
                InlineKeyboardButton(
                    text=choice.text,
                    callback_data=CallbackCodec.encode_payload({choice.key: True}),
                )
            )
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard


def build_delete_user_keyboard(stage: 'SelectStage', data: StageData)-> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    users = Users.get_all_users()
    for user in users:
        if user.chat_id == data.user.chat_id:
            continue
        user_data = {'user_id': user.chat_id}
        button = InlineKeyboardButton(
            text=f'Пользователь {user.chat_id}',
            callback_data=CallbackCodec.encode_payload(user_data)
        )
        keyboard.add(button)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard


def build_children_keyboard(stage: 'SelectStage', data: StageData) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if stage.children:
        for child in stage.children:
            if child.admin_only and not data.user.is_admin:
                continue
            keyboard.add(
                InlineKeyboardButton(
                    text=child.button_caption,
                    callback_data=CallbackCodec.encode_stage(child),
                )
            )
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard

def build_add_participant_keyboard(stage: "SelectStage", data: StageData)-> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    participant_ids = tuple(
        participant.person_id for participant in data.party.participants
    )
    for person in data.people:
        if person.id not in participant_ids:
            participant = {'participant_id': person.id}
            button_left = InlineKeyboardButton(
                text=person.with_coeff(),
                callback_data=CallbackCodec.encode_payload(
                    {
                        **participant,
                        'coeff': person.coeff
                    }
                )
            )
            button_right = InlineKeyboardButton(
                person.without_coeff(),
                callback_data=CallbackCodec.encode_payload(participant)
            )
            keyboard.add(button_left, button_right)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard

def build_remove_participant_keyboard(stage: 'SelectStage', data: StageData)-> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for participant in data.party.participants:
        participant_data = {'participant_id': participant.person_id}
        button = InlineKeyboardButton(
            text=participant.with_coeff_and_payment(),
            callback_data=CallbackCodec.encode_payload(participant_data)
        )
        keyboard.add(button)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard


def build_remove_person_keyboard(stage: 'SelectStage', data: StageData)-> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for person in data.people:
        person_data = {'person_id': person.id}
        button = InlineKeyboardButton(
            text=person.with_coeff(),
            callback_data=CallbackCodec.encode_payload(person_data)
        )
        keyboard.add(button)
    if stage.parent:
        keyboard.add(build_back_button(stage))
    return keyboard