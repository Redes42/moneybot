from copy import deepcopy
from dataclasses import field, dataclass

from entities.party import Party
from entities.participant import Participant

from decimal import Decimal

from entities.person import Person

@dataclass
class MoneyTransaction:
    sender: Participant
    recipient: Participant
    amount: Decimal = Decimal('0.0')


@dataclass
class Payments:
    lack_payers: list[Participant] = field(default_factory=list)
    over_payers: list[Participant] = field(default_factory=list)
    exact_payers: list[Participant] = field(default_factory=list)


@dataclass
class CalcResult:
    payments = Payments()
    final_pay: list[MoneyTransaction] = field(default_factory=list)
    avg_payment: Decimal = Decimal('0.0')


def calc_result(party: Party) -> CalcResult:
    party = deepcopy(party)
    result = CalcResult()
    payments: Payments = Payments()
    result.avg_payment = party.total_payment / party.total_coeff
    for participant in party.participants:
        if participant.payment < result.avg_payment * participant.coeff:
            payments.lack_payers.append(participant)
        elif participant.payment > result.avg_payment * participant.coeff:
            payments.over_payers.append(participant)
        else:
            payments.exact_payers.append(participant)

    result.payments = deepcopy(payments)

    for over_payer in payments.over_payers:
        for lack_payer in payments.lack_payers:
            rest = result.avg_payment * lack_payer.coeff - lack_payer.payment
            if over_payer.payment > result.avg_payment * over_payer.coeff:
                if over_payer.payment - rest >= result.avg_payment * over_payer.coeff:
                    over_payer.payment -= rest
                    lack_payer.payment += rest
                    transaction = MoneyTransaction(
                        lack_payer,
                        over_payer,
                        rest
                    )
                    result.final_pay.append(transaction)
                elif over_payer.payment - rest < result.avg_payment * over_payer.coeff:
                    lack_payer.payment += over_payer.payment - result.avg_payment * \
                                          over_payer.coeff
                    transaction = MoneyTransaction(
                        lack_payer,
                        over_payer,
                        over_payer.payment - result.avg_payment * over_payer.coeff
                    )
                    result.final_pay.append(transaction)
                    over_payer.payment = result.avg_payment * over_payer.coeff
            else:
                break
    return result



# party = Party()
# party.add_participant(Person(42, 'Имя'))
# party.participants[-1].payment = Decimal('123')
# party.add_participant(Person(43, 'Имя2'))
# party.participants[-1].payment = Decimal('200')
# party.add_participant(Person(44, 'Имя3'))
# party.participants[-1].payment = Decimal('350')
# print(calc_result(party))


