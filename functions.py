from decimal import Decimal

from bot import bot
from db import get_people
from party import parties, Party
from person import people, Person


def get_user_name(chat_id: int) -> str:
    return bot.get_chat(chat_id).first_name

def new_party(chat_id: int):
    parties[chat_id] = Party()
    people[chat_id] = get_people(chat_id)

def clean_party(chat_id: int):
    parties[chat_id] = Party()

def get_added_people(chat_id: int) -> str:
    added_people = parties[chat_id].people
    added_people_str = '\n'
    if added_people:
        added_people_str = added_people_str.join(person.name for person in added_people)
    else:
        added_people_str += '\\-\\- никого \\-\\-'
    return 'Уже добавлены:\n' + added_people_str + '\n\n'

def add_participant(chat_id: int, person_id: int):
    for person in people[chat_id]:
        if person.id == person_id:
            if person not in parties[chat_id].people:
                parties[chat_id].people.append(person)

def define_coeff(chat_id: int, coeff: float):
    parties[chat_id].people[-1].coeff = coeff

def define_payment(chat_id: int, payment: Decimal):
    parties[chat_id].people[-1].payment = payment
