from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Callable, Tuple, TypeAlias

from telebot import types, formatting
from unicodedata import decimal

from bot import bot
from functions import new_party, get_added_people, define_coeff, \
    define_payment, add_participant, clean_party, get_user_name
from keyboards import create_participants_keyboard
from party import parties
from person import Person, people
from stages import Stages

Func: TypeAlias = (
        Callable[[types.Message], None] |
        Callable[[int, int | Decimal | float | str], None] |
        None
    )

@dataclass
class Stage:
    title: str = ''
    text: str = ''
    command: str = ''
    get_inner_text: Callable[[int], str] = None
    func: Func = None

    def process(self, message: types.Message):
        raise NotImplementedError


    def send_stage_message(
            self, chat_id: int, inner_text: str='', keyboard: types.InlineKeyboardMarkup=None
    ):
        bot.send_message(
            chat_id=chat_id,
            text=formatting.format_text(
                formatting.mbold(self.title),
                '\n' + inner_text + self.text),
            reply_markup=keyboard,
            parse_mode='MarkdownV2'
        )

    def send_text_message(self, chat_id: int, text: str):
        bot.send_message(
            chat_id=chat_id,
            text=text,
        )


@dataclass
class SelectStage(Stage):
    parent: str | None = None
    children: Tuple[Stages, ...] | None = None

    def create_keyboard(self, message: types.Message) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        for child in self.children:
            button = types.InlineKeyboardButton(text=MENU[child].title, callback_data=str(MENU[child].command))
            keyboard.add(button)
        if self.parent is not None:
            button = types.InlineKeyboardButton('< Назад', callback_data=self.parent)
            keyboard.add(button)
        return keyboard

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


@dataclass
class CustomSelectStage(SelectStage):

    def create_keyboard(self, message: types.Message) -> types.InlineKeyboardMarkup:
        if self.command == Stages.ADD_PARTICIPANT:
            return create_participants_keyboard(people[message.chat.id])


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


MENU: dict[str, Stage | SelectStage | CustomSelectStage | InputStage] = {
    Stages.START: SelectStage(
        title='Бот для взаиморасчётов по деньгам, потраченным на вечеринку',
        text=', добро пожаловать\\!',
        command=Stages.START,
        children=(Stages.MAIN_MENU,),
        get_inner_text=get_user_name,
        func=new_party
    ),
    Stages.MAIN_MENU: SelectStage(
        title='Главное меню',
        text='Выберите опцию:',
        command=Stages.MAIN_MENU,
        parent=Stages.START,
        children=(Stages.NEW_PARTY, Stages.EDIT_PEOPLE),
    ),
    Stages.NEW_PARTY: SelectStage(
        title='Новая вечеринка',
        text='Начало расчёта \\- добавьте людей, определите для них коэффициент и затраченные суммы',
        command=Stages.NEW_PARTY,
        func=clean_party,
        children=(Stages.ADD_PARTICIPANT, Stages.CALC_RESULT),
        parent=Stages.MAIN_MENU
    ),
    Stages.EDIT_PEOPLE: SelectStage('Редактировать базу людей', Stages.EDIT_PEOPLE, None, None, Stages.MAIN_MENU),
    Stages.ADD_PERSON: CustomSelectStage(),
    Stages.REMOVE_PERSON: CustomSelectStage(),
    Stages.ADD_PARTICIPANT: CustomSelectStage(
        title='Добавить людей на вечеринку',
        text='Выберите ещё людей из сохранённого списка:',
        command=Stages.ADD_PARTICIPANT,
        get_inner_text=get_added_people,
        children=(Stages.DEFINE_COEFF, Stages.DEFINE_PAYMENT),
        parent=Stages.NEW_PARTY
    ),
    Stages.DEFINE_COEFF: InputStage(
        title='Укажите коэффициент для участника:',
        text='В формате дробного числа, например 1\\.0 \\(это 100%\\) или 0\\.5 \\(это 50%\\) или 2\\.0 \\(это 200%\\)'
             'Обычно используется 100%, 200% нужны для семей из двух человек, 50 \\- для тех кто мало ел',
        command=Stages.DEFINE_COEFF,
        preprocess_func=add_participant,
        func=define_coeff,
        child=Stages.DEFINE_PAYMENT,
        input_type=float
    ),
    Stages.DEFINE_PAYMENT: InputStage(
        title='Укажите платёж участника:',
        text='В формате дробного числа, например 123\\.56',
        command=Stages.DEFINE_PAYMENT,
        preprocess_func=add_participant,
        func=define_payment,
        child=Stages.ADD_PARTICIPANT,
        input_type=Decimal
    ),
    Stages.REMOVE_PARTICIPANT: SelectStage(),
    Stages.CALC_RESULT: SelectStage(
        title='Произвести расчёт',
        text='',
        command=Stages.CALC_RESULT,
        func=None,
        parent=Stages.NEW_PARTY)
}
