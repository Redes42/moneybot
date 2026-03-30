from app.people_ops import next_person_id, update_person_coeff, update_person_name
from domain.party import Party
from domain.person import Person
from stage_data import StageData

class BaseStageLogic:
    """
    Базовый класс бизнес-логики стадии.

    Logic-объект:
    - не знает про FlowManager
    - не знает про Menu
    - не делает переходы
    - просто модифицирует StageData
    """

    def preprocess(self, data: StageData) -> None:
        pass

    def process(self, data: StageData, value: object | None = None) -> None:
        pass


class EmptyStageLogic(BaseStageLogic):
    pass



class StartNewPartyLogic(BaseStageLogic):
    def preprocess(self, data: StageData) -> None:
        data.party = Party()


class AddParticipantStageLogic(BaseStageLogic):
    def process(self, data: StageData, value: object | None = None) -> None:
        if value is None:
            raise ValueError("Не передан id участника")

        person_id = int(value)
        person = next((person for person in data.people if person.id == person_id), None)
        if person is None:
            raise ValueError("Человек не найден")

        if data.party is None:
            data.party = Party()

        data.party.add_participant(person)


class SetCoeffLogic(BaseStageLogic):
    def process(self, data: StageData, value: object | None = None) -> None:
        if value is None:
            raise ValueError("Не передано значение коэффициента")
        if data.party is None:
            raise ValueError("Вечеринка не создана")

        participant_id = int(data.pending_payload["participant_id"])
        participant = data.party.get_participant(participant_id)
        participant.set_coeff(float(value))
        data.pending_payload = {}


class SetPaymentLogic(BaseStageLogic):
    def process(self, data: StageData, value: object | None = None) -> None:
        if value is None:
            raise ValueError("Не передано значение платежа")
        if data.party is None:
            raise ValueError("Вечеринка не создана")

        participant_id = int(data.pending_payload["participant_id"])
        participant = data.party.get_participant(participant_id)
        participant.set_payment(value)
        data.pending_payload = {}


class AddPersonLogic(BaseStageLogic):
    def process(self, data: StageData, value: object | None = None) -> None:
        if value is None:
            raise ValueError("Имя не передано")

        new_id = next_person_id(data.people)
        data.people.append(Person(id=new_id, name=str(value), coeff=1.0))


class EditPersonNameLogic(BaseStageLogic):
    def process(self, data: StageData, value: object | None = None) -> None:
        if value is None:
            raise ValueError("Имя не передано")

        person_id = int(data.pending_payload["person_id"])
        update_person_name(data.people, person_id, str(value))
        data.pending_payload = {}


class EditPersonCoeffLogic(BaseStageLogic):
    def process(self, data: StageData, value: object | None = None) -> None:
        if value is None:
            raise ValueError("Коэффициент не передан")

        person_id = int(data.pending_payload["person_id"])
        update_person_coeff(data.people, person_id, float(value))
        data.pending_payload = {}
