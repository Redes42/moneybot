from dataclasses import dataclass
from html import escape
from enum import StrEnum

from bot.safe_sender import send_safe_message
from flow.stage_data import StageData
from logic.keyboards import KeyboardBuilder, build_children_keyboard
from logic.stage_logic import BaseStageLogic
from logic.text_factories import TextFactory
from flow.validators import BaseValidator

class Stages(StrEnum):
    START = 'start'
    MAIN_MENU = 'main_menu'
    EDIT_PEOPLE = 'edit_people'
    ADD_PERSON = 'add_person'
    DEFINE_NAME = 'define_name'
    REMOVE_PERSON = 'remove_person'
    NEW_PARTY = 'new_party'
    ADD_PARTICIPANT = 'add_participant'
    DEFINE_COEFF = 'define_coeff'
    DEFINE_PAYMENT = 'define_payment'
    REMOVE_PARTICIPANT = 'remove_participant'
    CALC_RESULT = 'calc_result'


@dataclass(eq=False)
class Stage:
    title: str = ''
    text: str = ''
    name: str = ''
    parent: "Stage | None" = None
    children: tuple["Stage"] | None = None
    logic: BaseStageLogic | None = None
    text_factory: TextFactory | None = None

    def preprocess(self, data: StageData) -> None:
        if self.logic:
            self.logic.preprocess(data)

    def _build_text(self, data: StageData):
        msg = [f'<b>{escape(self.title)}:</b>']
        inner_text = ''
        if self.text_factory:
            inner_text = self.text_factory(data)
        msg.append('\n' + inner_text + escape(self.text))
        return '\n'.join(msg)

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        send_safe_message(data.chat_id, msg)

    def process(self, data: StageData) -> bool:
        if self.logic:
            self.logic.process(data)
        return True


@dataclass(eq=False)
class SelectStage(Stage):
    keyboard_builder: KeyboardBuilder | None = build_children_keyboard

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        keyboard = None
        if self.keyboard_builder:
            keyboard = self.keyboard_builder(self, data)
        send_safe_message(data.chat_id, msg, keyboard)


@dataclass(eq=False)
class InputStage(Stage):
    validators: tuple[BaseValidator, ...] = tuple(),

    def process(self, data: StageData) -> bool:
        current_value = data.payload.get('value')
        try:
            for validator in self.validators:
                current_value = validator.validate(current_value)
        except ValueError as exc:
            data.messages.append(str(exc))
            return False
        if self.logic:
            self.logic.process(data, current_value)
        return True
