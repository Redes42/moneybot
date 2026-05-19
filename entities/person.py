from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Person:
    """
    Immutable запись базы людей.

    Почему frozen=True:
    - Person — это справочная сущность, а не runtime-состояние.
    - Нельзя случайно изменить имя или default coeff в произвольной части кода.
    - При редактировании создаётся новый объект через dataclasses.replace(...).
    """
    id: int
    name: str
    coeff: float = 1.0

    @staticmethod
    def format_coeff(coeff: float) -> Decimal:
        decimal_coeff = Decimal(coeff)
        return decimal_coeff.quantize(Decimal('0.0'), ROUND_HALF_UP)

    def with_coeff(self) -> str:
        return f'{self.name} ({Person.format_coeff(self.coeff)})'

    def without_coeff(self) -> str:
        return f'{self.name} (без к-та)'