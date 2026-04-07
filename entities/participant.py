from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Participant:
    """
    Snapshot-сущность участника вечеринки.

    Это не Person и не наследник Person. Участник хранит состояние именно
    внутри конкретной вечеринки:
    - person_id: связь с человеком из базы
    - name: снимок имени на момент добавления
    - coeff: рабочий коэффициент в рамках этой вечеринки
    - payment: фактический платёж в рамках этой вечеринке

    Такой подход полезен тем, что редактирование Person в базе не
    переписывает старые вечеринки автоматически.
    """
    person_id: int
    name: str
    coeff: float = 1.0
    payment: Decimal = Decimal("0")

    def with_coeff(self):
        return f'{self.name} ({self.coeff})'

    def without_coeff(self):
        return f'{self.name} (?)'

    def with_coeff_and_payment(self):
        return f'{self.name} ({self.coeff}, {self.payment} руб.)'

