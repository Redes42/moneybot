from dataclasses import dataclass
from decimal import Decimal

from bot.log import info
from entities.people_ops import update_person_coeff, update_person_name, get_person
from db.app import Persons, Users
from entities.person import Person
from flow.stage_data import StageData
from logic.keyboards import Choice


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


class SkipStageLogic(BaseStageLogic):
    def preprocess(self, data: StageData) -> PreprocessResult:
        return PreprocessResult(skip_current_stage=True)


class DefineChatIdStageLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        chat_id = data.payload.get('value')
        if chat_id is None:
            raise ValueError('Не передано значение chat_id')
        data.payload['user_id'] = chat_id


class ChooseIsAdminStageLogic(BaseStageLogic):
    def preprocess(self, data: StageData) -> PreprocessResult:
        data.payload.update(
            {
                'choices': (Choice('yes', 'Да'), Choice('no', 'Нет'))
            }
        )
        return PreprocessResult()

    def process(self, data: StageData) -> None:
        user_id = data.payload.get('user_id')
        if user_id is None:
            raise ValueError('Не передано значение user_id')
        if data.payload.get('yes'):
            Users.create_user(chat_id=user_id, is_admin=True)
        if data.payload.get('no'):
            Users.create_user(chat_id=user_id, is_admin=False)
        if data.payload.get('choices'):
            del data.payload['choices']


class DeleteUserStageLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        user_id = data.payload.get('user_id')
        if user_id is None:
            raise ValueError('Не передан id пользователя')
        Users.delete_user(chat_id=user_id)


class ClearPartyLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        if data.party:
            info(data=data, message='Cleared current party')
            data.party.clear()


class AddParticipantStageLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        participant_id = data.payload.get('participant_id')
        if participant_id is None:
            raise ValueError('Не передан id участника')
        person = get_person(data.people, int(participant_id))
        if person is None:
            raise ValueError('Человек не найден')
        success = data.party.add_participant(person)
        if not success:
            raise ValueError('Участник уже добавлен!')
        else:
            info(data=data, message=f'Added participant')


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
        participant.coeff = Decimal(coeff)


class SetPaymentLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        payment = data.payload.get('value')
        if payment is None:
            raise ValueError('Не передано значение платежа')
        participant_id = data.payload['participant_id']
        participant = data.party.get_participant(participant_id)
        participant.payment = Decimal(payment)


class RemoveParticipantStageLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        participant_id = data.payload.get('participant_id')
        if participant_id is None:
            raise ValueError('Не передан id участника')
        success = data.party.remove_participant(int(participant_id))
        if not success:
            raise ValueError('Участник не найден!')


class AddPersonWithCoeffLogic(BaseStageLogic):
    def preprocess(self, data: StageData) -> PreprocessResult:
        return PreprocessResult(skip_current_stage=True)


class AddPersonWithoutCoeffLogic(BaseStageLogic):
    def preprocess(self, data: StageData) -> PreprocessResult:
        data.payload['coeff'] = Decimal('1.0')
        return PreprocessResult(skip_current_stage=True)


class SetPersonNameLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        name = data.payload.get('value')
        if name is None:
            raise ValueError('Не указано имя участника')
        data.payload['name'] = name


class SetPersonCoeffLogic(BaseStageLogic):
    def add_person(self, data: StageData):
        if 'name' not in data.payload:
            raise ValueError('Не указано имя участника')
        person = Person(0, data.payload['name'], data.payload['coeff'])
        person = Persons.create_person(data.user.chat_id, person)
        data.people.append(person)

    def preprocess(self, data: StageData) -> PreprocessResult:
        if 'coeff' in data.payload:
            self.add_person(data)
            return PreprocessResult(skip_current_stage=True)
        return PreprocessResult()

    def process(self, data: StageData) -> None:
        data.payload['coeff'] = data.payload.get('value')
        self.add_person(data)


class RemovePersonLogic(BaseStageLogic):
    def process(self, data: StageData) -> None:
        person_id = data.payload.get('person_id')
        if person_id is None:
            raise ValueError('Не указан id человека')
        person = get_person(data.people, person_id)
        data.people.remove(person)
        Persons.delete_person(person)