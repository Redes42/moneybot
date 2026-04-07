from html import escape
from typing import Callable, TypeAlias

from bot import bot
from flow.stage_data import StageData

type TextFactory = Callable[[StageData], str]
#TextFactory: TypeAlias = Callable[[StageData], str]

def get_user_name(data: StageData) -> str:
    return escape(bot.get_chat(data.chat_id).first_name)

def get_added_people(data: StageData) -> str:
    added_people = '\n'
    if data.people:
        added_people = added_people.join(person.name for person in data.people)
    else:
        added_people += '\\-\\- никого \\-\\-'
    added_people = escape(added_people)
    return f'Уже добавлены:\n' + added_people + '\n\n'

