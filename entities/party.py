from dataclasses import dataclass, field
from decimal import Decimal

from entities.person import Person
from entities.participant import Participant

@dataclass
class Party:
    """
    Текущая вечеринка пользователя.

    Party хранит только participants текущей вечеринки.
    База людей пользователя живёт отдельно в UserSession.people.

    Это важное и полезное разделение:
    - people = справочник
    - participants = конкретные участники текущей вечеринки
    """
    participants: list[Participant] = field(default_factory=list)

    def add_participant(self, person: Person) -> bool:
        if any(participant.person_id == person.person_id for participant in self.participants):
            return False
        self.participants.append(
            Participant(
                person_id=person.person_id,
                name=person.name,
                coeff=person.coeff,
            )
        )
        return True

    def get_participant(self, person_id: int) -> Participant:
        for participant in self.participants:
            if participant.person_id == person_id:
                return participant
        raise ValueError("Участник не найден")

    @property
    def people_count(self) -> int:
        return len(self.participants)

    @property
    def total_payment(self) -> Decimal:
        return sum((participant.payment for participant in self.participants), start=Decimal("0"))

    @property
    def total_coeff(self) -> float:
        return sum(participant.coeff for participant in self.participants)
