from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Person:
    id: int = 0
    name: str = ''
    coeff: float = 1.0
    payment: Decimal = Decimal('0.0')

    def with_coeff(self):
        return f'{self.name} ({self.coeff})'

    def without_coeff(self):
        return f'{self.name} (?)'


people: dict[int, list[Person]] = {}