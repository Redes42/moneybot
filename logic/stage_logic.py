from dataclasses import dataclass

from app.people_ops import update_person_coeff, update_person_name, get_person
from db.db import get_people
from entities.party import Party
from entities.person import Person
from flow.stage_data import StageData

@dataclass
class PreprocessResult:
    skip_current_stage: bool = False

class BaseStageLogic:
    """
    Базовый класс бизнес-логики стадии.

    Logic-объект:
    - не знает про FlowManager
    - не знает про Menu
    - не делает переходы
    - просто модифицирует StageData
    """

    def preprocess(self, data: StageData) -> PreprocessResult:
        return PreprocessResult()

    def process(self, data: StageData) -> None:
        pass


class NewPartyLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        if data.party:
            data.party.clear()


class AddParticipantStageLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        if data.payload.get('participant_id') is None:
            raise ValueError('Не передан id участника')
        person_id = int(data.payload['participant_id'])
        person = get_person(data.people, person_id)
        if person is None:
            raise ValueError('Человек не найден')
        success = data.party.add_participant(person)
        if not success:
            raise ValueError('Участник уже добавлен!')


class SetCoeffLogic(BaseStageLogic):
    def preprocess(self, data: StageData) -> PreprocessResult:
        if 'coeff' in data.payload:
            return PreprocessResult(skip_current_stage=True)
        return PreprocessResult()

    def process(self, data: StageData) -> None:
        coeff = data.payload.get('value')
        if coeff is None:
            raise ValueError('Не передано значение коэффициента')
        participant_id = data.payload['participant_id']
        participant = data.party.get_participant(participant_id)
        participant.coeff = coeff


class SetPaymentLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        payment = data.payload.get('value')
        if payment is None:
            raise ValueError('Не передано значение платежа')
        participant_id = data.payload['participant_id']
        participant = data.party.get_participant(participant_id)
        participant.payment = payment


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
