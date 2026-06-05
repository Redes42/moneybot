from dataclasses import dataclass
from html import escape
from enum import StrEnum
from typing import Optional

from telebot.types import InlineKeyboardMarkup

from bot.log import error, info, debug, warning
from bot.safe_sender import send_safe_message
from flow.stage_data import StageData
from logic.keyboards import KeyboardBuilder, build_children_keyboard, \
    build_back_button
from logic.image_factories import ImageFactory
from logic.stage_logic import BaseStageLogic, PreprocessResult
from logic.text_factories import TextFactory
from flow.validators import BaseValidator

class Stages(StrEnum):
    START = 'start'
    MAIN_MENU = 'main_menu'
    ADMIN_MENU = 'admin_menu'
    CREATE_USER = 'create_user'
    DEFINE_CHAT_ID = 'define_chat_id'
    CHOOSE_IS_ADMIN = 'choose_is_admin'
    DELETE_USER = 'delete_user'
    HELP = 'help'
    EDIT_PEOPLE = 'edit_people'
    ADD_PERSON_WITH_COEFF = 'add_person_with_coeff'
    ADD_PERSON_WO_COEFF = 'add_person_wo_coeff'
    DEFINE_PERSON_NAME = 'define_person_name'
    DEFINE_PERSON_COEFF = 'define_person_coeff'
    REMOVE_PERSON = 'remove_person'
    CURRENT_PARTY = 'current_party'
    ADD_PARTICIPANT = 'add_participant'
    DEFINE_PARTICIPANT_COEFF = 'define_participant_coeff'
    DEFINE_PARTICIPANT_PAYMENT = 'define_participant_payment'
    REMOVE_PARTICIPANT = 'remove_participant'
    CALC_RESULT_FULL = 'calc_result_full'
    CALC_RESULT_SHORT = 'calc_result_short'


@dataclass(eq=False)
class Stage:
    title: str = ''
    text: str = ''
    name: str = ''
    parent: "Stage | None" = None
    children: tuple["Stage"] | None = None
    default_child: "Stage | None" = None
    logic: Optional[BaseStageLogic] | None = None
    text_factory: Optional[TextFactory] = None
    image_factory: Optional[ImageFactory] = None
    clear_payload_on_success: bool = False
    admin_only: bool = False

    def preprocess(self, data: StageData) -> PreprocessResult:
        if self.logic:
            return self.logic.preprocess(data)
        return PreprocessResult()

    def _build_text(self, data: StageData) -> str:
        msg = [f'<b>{escape(self.title)}</b>']
        inner_text = ''
        if self.text_factory:
            inner_text = self.text_factory(data)
        msg.append('\n' + inner_text + escape(self.text))
        return '\n'.join(msg)

    def _build_image(self, data: StageData) -> Optional[str]:
        if self.image_factory:
            image_id = self.image_factory(data)
            return image_id
        return None

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        img = self._build_image(data)
        send_safe_message(data.user.chat_id, msg, image_id=img)

    def process(self, data: StageData) -> bool:
        if self.logic:
            self.logic.process(data)
        return True


@dataclass(eq=False)
class SelectStage(Stage):
    keyboard_builder: KeyboardBuilder | None = build_children_keyboard
    button_caption: str | None = None

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        img = self._build_image(data)
        keyboard = None
        if self.keyboard_builder:
            keyboard = self.keyboard_builder(self, data)
            debug(self, data, message='Built keyboard')
        send_safe_message(data.user.chat_id, msg, keyboard, image_id=img)


@dataclass(eq=False)
class InputStage(Stage):
    validators: tuple[BaseValidator, ...] = tuple(),
    show_back_button: bool = False

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        img = self._build_image(data)
        keyboard = None
        if self.show_back_button:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(build_back_button(self))
        send_safe_message(data.user.chat_id, msg, keyboard, image_id=img)

    def process(self, data: StageData) -> bool:
        current_value = data.payload.get('value')
        current_validator: Optional[BaseValidator] = None
        try:
            for validator in self.validators:
                current_validator = validator
                current_value = validator.validate(current_value)
            data.payload['value'] = current_value
        except ValueError as exc:
            warning(
                self,
                data,
                message=f'Validation error from {current_validator.__class__.__name__}'
            )
            send_safe_message(data.user.chat_id, str(exc))
            return False
        if self.logic:
            self.logic.process(data)
        return True
