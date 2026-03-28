from person import Person
from stages import Stages


class Party:
    def __init__(self, stage: Stages=Stages.START, people: list[Person]=None):
        self.stage = stage
        if people is not None:
            self.people: list[Person] = people
        else:
            self.people: list[Person] = []


    @property
    def people_count(self) -> int:
        if self.people:
            result = 0.0
            for person in self.people:
                result += person.coeff
        else:
            return 0

parties: dict[int, Party] = {}