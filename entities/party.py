from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP

from mako.testing.helpers import result_lines

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
        if any(participant.person_id == person.id for participant in self.participants):
            return False
        self.participants.append(
            Participant(
                person_id=person.id,
                name=person.name,
                coeff=Decimal(str(person.coeff)),
            )
        )
        return True

    def get_participant(self, person_id: int) -> Participant:
        for participant in self.participants:
            if participant.person_id == person_id:
                return participant
        raise ValueError("Участник не найден")

    def remove_participant(self, participant_id: int) -> bool:
        participant = self.get_participant(participant_id)
        self.participants.remove(participant)
        return True

    def clear(self):
        self.participants = []

    @property
    def participant_count(self) -> int:
        result = 0
        for participant in self.participants:
            result += int(participant.coeff.quantize(
                Decimal('1'), rounding=ROUND_HALF_UP)
            )
        return result

    @property
    def total_payment(self) -> Decimal:
        return sum((participant.payment for participant in self.participants), start=Decimal('0'))

    @property
    def total_coeff(self) -> Decimal:
        return sum((participant.coeff for participant in self.participants), start=Decimal('0'))
