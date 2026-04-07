from decimal import Decimal

from bot import bot
from db.db import get_people
from entities.party import parties, Party
from entities.person import people




def add_participant(chat_id: int, person_id: int):
    for person in people[chat_id]:
        if person.person_id == person_id:
            if person not in parties[chat_id].people:
                parties[chat_id].people.append(person)

def define_coeff(chat_id: int, coeff: float):
    parties[chat_id].people[-1].coeff = coeff

def define_payment(chat_id: int, payment: Decimal):
    parties[chat_id].people[-1].payment = payment
