from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Person:
    """
    Immutable запись базы людей.

    Почему frozen=True:
    - Person — это справочная сущность, а не runtime-состояние.
    - Нельзя случайно изменить имя или default coeff в произвольной части кода.
    - При редактировании создаётся новый объект через dataclasses.replace(...).
    """
    person_id: int
    name: str
    coeff: float = 1.0

    def with_coeff(self):
        return f'{self.name} ({self.coeff})'

    def without_coeff(self):
        return f'{self.name} (?)'