from decimal import Decimal, ROUND_HALF_UP
from html import escape
from itertools import chain
from typing import Callable

from bot import bot
from entities.participant import Participant
from flow.stage_data import StageData
from logic.calc import calc_result, CalcResult


type TextFactory = Callable[[StageData], str]


tab = '    '


def get_persons_list(data: StageData) -> str:
    if not data.people:
        return '<i>База людей пуста</i>'
    else:
        people = '<b>Уже в базе:</b>\n'
        for person in data.people:
            people += f'{tab}{person.with_coeff()}\n'
        return f'{people}\n'


def get_user_name(data: StageData) -> str:
    return escape(bot.get_chat(data.user.chat_id).first_name)


def get_help(data: StageData) -> str:
    return '!'


def get_participants(data: StageData) -> str:
    participants = '\n'
    if data.party.participants:
        participants = participants.join(
            f'{tab}{participant.with_coeff_and_payment()}' for participant in data.party.participants
        )
    else:
        participants += f'{tab}-- никого --'
    participants = escape(participants)
    return f'Уже добавлены: {participants} \n\n'


def get_full_calc_result(data: StageData) -> str:

    def format_payment(payment: Decimal) -> Decimal:
        return payment.quantize(Decimal('0.00'), ROUND_HALF_UP)

    def get_payers(calc: CalcResult) -> chain[Participant]:
        return chain(
            calc.payments.over_payers,
            calc.payments.lack_payers,
            calc.payments.exact_payers
        )

    rub = 'руб.'
    result = 'Участники отсутствуют, расчёт невозможен! Добавьте участников.'
    party = data.party
    if not party.participants:
        return result
    calc: CalcResult = calc_result(party)

    result = f'<b>Суммарные расходы:</b> {format_payment(party.total_payment)} {rub}\n'
    result += f'<b>Количество человек</b>: {party.participant_count}\n'
    result += f'<b>Средний платёж</b>: {format_payment(calc.avg_payment)} {rub}\n'

    result += '\n<b>Расходы до расчётов</b>:\n'
    payers = get_payers(calc)
    for payer in payers:
        pay_verb_form = 'заплатил(а)'
        if payer.coeff >= Decimal('1.5'):
            pay_verb_form = 'заплатили'
        payer_with_verb = f'{payer.name} {pay_verb_form}'
        pay_sub_result = (
            f'{payer_with_verb} {format_payment(payer.payment)} {rub} '
            f'(на {abs(
                format_payment(payer.payment - calc.avg_payment * payer.coeff)
            )} {rub}'
        )
        if payer.payment > calc.avg_payment * payer.coeff:
            result += f'{tab}{pay_sub_result} больше)\n'
        elif Decimal('0.0') < payer.payment < calc.avg_payment * payer.coeff:
            result += f'{tab}{pay_sub_result} меньше)\n'
        elif payer.payment == calc.avg_payment * payer.coeff:
            result += (
                f'{tab}{payer_with_verb} {format_payment(payer.payment)} '
                '(ровно как надо)\n'
            )
        else:
            result += f'{tab}{payer.name} ничего не {pay_verb_form}\n'

    result += '\n<b>Необходимые переводы</b>:\n'
    if not calc.final_pay:
        result += f'{tab}Не требуются, все заплатили поровну\n'
    for transaction in calc.final_pay:
        if transaction.amount != Decimal('0.0'):
            result += (
                f'{tab}{transaction.sender.name} --> '
                f'{transaction.recipient.name}: '
                f'{format_payment(transaction.amount)} {rub}\n'
            )

    result += '\n<b>Расходы после расчётов</b>:\n'
    payers = get_payers(calc)
    for payer in payers:
        pay_verb_form = 'заплатит'
        if payer.coeff >= Decimal('1.5'):
            pay_verb_form = 'заплатят'
        result += (
            f'{tab}В итоге {payer.with_coeff()} {pay_verb_form} '
            f'{format_payment(calc.avg_payment * payer.coeff)} {rub}\n'
        )

    return result


def get_short_calc_result(data: StageData) -> str:

    def format_payment(payment: Decimal) -> Decimal:
        return payment.quantize(Decimal('0.00'), ROUND_HALF_UP)

    rub = 'руб.'
    result = 'Участники отсутствуют, расчёт невозможен! Добавьте участников.'
    party = data.party
    if not party.participants:
        return result
    calc: CalcResult = calc_result(party)

    result = f'<b>Суммарные расходы:</b> {format_payment(party.total_payment)} {rub}\n'
    result += f'<b>Количество человек</b>: {party.participant_count}\n'
    result += f'<b>Средний платёж</b>: {format_payment(calc.avg_payment)} {rub}\n'

    result += '\n<b>Необходимые переводы</b>:\n'
    if not calc.final_pay:
        result += f'{tab}Не требуются, все заплатили поровну\n'
    for transaction in calc.final_pay:
        if transaction.amount != Decimal('0.0'):
            result += (
                f'{tab}{transaction.sender.name} --> '
                f'{transaction.recipient.name}: '
                f'{format_payment(transaction.amount)} {rub}\n'
            )

    return result
