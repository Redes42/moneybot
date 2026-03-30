from dataclasses import dataclass
from html import escape
from enum import StrEnum

from bot.bot import send_safe_message
from stage_data import StageData
from stage_logic import BaseStageLogic

class Stages(StrEnum):
    START = 'start'
    MAIN_MENU = 'main_menu'
    EDIT_PEOPLE = 'edit_people'
    ADD_PERSON = 'add_person'
    REMOVE_PERSON = 'remove_person'
    NEW_PARTY = 'new_party'
    ADD_PARTICIPANT = 'add_participant'
    DEFINE_COEFF = 'define_coeff'
    DEFINE_PAYMENT = 'define_payment'
    REMOVE_PARTICIPANT = 'remove_participant'
    CALC_RESULT = 'calc_result'


@dataclass
class Stage:
    title: str = ''
    text: str = ''
    command: str = ''
    logic: BaseStageLogic | None = None,
    text_factory: "TextFactory | None" = None,

    def preprocess(self, data: StageData) -> None:
        if self.logic:
            self.logic.preprocess(data)

    def _build_text(self, data: StageData):
        msg = [f'<b>{escape(self.title)}:</b>']
        if self.text_factory:
            inner_text = self.text_factory(data)
            msg.extend(inner_text)
        msg.extend(self.text)
        return "<br>".join(msg)

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        send_safe_message(data.chat_id, msg)

    def process(self, data: StageData) -> bool:
        if self.logic:
            self.logic.process(data)
        return True


@dataclass
class SelectStage(Stage):
    keyboard_builder: "BaseKeyboardBuilder | None" = None

    def render_message(self, data: StageData):
        msg = self._build_text(data)
        keyboard = None
        if self.keyboard_builder:
            keyboard = self.keyboard_builder.build(self, data)
        send_safe_message(data.chat_id, msg, keyboard)



    def process(self, message: types.Message):
        chat_id = message.chat.id
        inner_text = ''
        if self.get_inner_text is not None:
            inner_text = self.get_inner_text(message.chat.id)
        keyboard: types.InlineKeyboardMarkup = self.create_keyboard(message)
        self.send_stage_message(chat_id, inner_text, keyboard)
        if self.func is not None:
            self.func(chat_id)
        parties[chat_id].stage = self.command


class SelectStage(Stage):
    def __init__(
        self,
        title: str,
        text: str = "",
        logic: BaseStageLogic | None = None,
        text_factory: "TextFactory | None" = None,
        keyboard_builder: "BaseKeyboardBuilder | None" = None,
    ) -> None:
        super().__init__(title, text, logic, text_factory)
        self.keyboard_builder = keyboard_builder

    def prompt(self, bot: TeleBot, data: StageData, menu: Menu) -> None:
        text = self.build_text(data)
        keyboard = None

        if self.keyboard_builder:
            keyboard = self.keyboard_builder.build(self, data, menu)

        send_safe_message(bot, data.chat_id, text, reply_markup=keyboard)

    def process(self, data: StageData, value: object | None = None) -> bool:
        if self.logic:
            self.logic.process(data, value)
        return True


@dataclass
class InputStage(Stage):
    input_type: type = float
    preprocess_func: Callable[[int, int], None] = None
    child: Stages | None = None

    def preprocess(self, message: types.Message, param: int = 0):
        chat_id = message.chat.id
        parties[chat_id].stage = self.command
        self.send_stage_message(chat_id)
        if self.preprocess_func is not None:
            self.preprocess_func(chat_id, param)
        parties[chat_id].stage = self.command

    def process(self, message: types.Message) -> bool:
        chat_id = message.chat.id
        try:
            result = self.input_type(message.text)
            if self.func is not None:
                self.func(chat_id, result)
            return True
        except (ValueError, InvalidOperation):
            self.send_text_message(message.chat.id, 'Ошибка ввода, введите дробное или целое число')
            return False


class InputStage(Stage):
    def __init__(
        self,
        title: str,
        text: str = "",
        logic: BaseStageLogic | None = None,
        text_factory: "TextFactory | None" = None,
        validators: tuple[BaseValidator, ...] = tuple(),
        prompt_text: str = "",
    ) -> None:
        super().__init__(title, text, logic, text_factory)
        self.validators = validators
        self.prompt_text = prompt_text

    def build_text(self, data: StageData) -> str:
        parts = [self.title]

        if self.text_factory:
            dynamic_text = self.text_factory(data)
            if dynamic_text:
                parts.append(dynamic_text)
        elif self.prompt_text:
            parts.append(self.prompt_text)
        elif self.text:
            parts.append(self.text)

        return "\n\n".join(part for part in parts if part)

    def process(self, data: StageData, value: object | None = None) -> bool:
        current_value = value

        try:
            for validator in self.validators:
                current_value = validator.validate(current_value)
        except ValueError as exc:
            data.messages.append(str(exc))
            return False

        if self.logic:
            self.logic.process(data, current_value)

        return True