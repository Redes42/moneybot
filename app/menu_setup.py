from logic.stage_logic import (
    AddParticipantStageLogic,
    AddPersonLogic,
    EditPersonCoeffLogic,
    EditPersonNameLogic,
    SetCoeffLogic,
    SetPaymentLogic,
    NewPartyLogic,
)
from flow.stages import Stages, InputStage, SelectStage, Stage
#from app.text_factories import input_coeff_text_factory, input_payment_text_factory, new_party_text_factory
from logic.keyboards import build_add_participant_keyboard, build_remove_participants_keyboard
from logic.text_factories import get_user_name, get_added_people
from flow.menu import Menu
from flow.validators import NonEmptyStringValidator, NonNegativeDecimalValidator, PositiveFloatValidator


def build_menu() -> Menu:

    start = SelectStage(
        title='Бот для взаиморасчётов по деньгам, потраченным на вечеринку',
        text=', добро пожаловать!',
        name=Stages.START,
        text_factory=get_user_name,
    )
    main_menu = SelectStage(
        title='Главное меню',
        text='Выберите действие:',
        name=Stages.MAIN_MENU,
    )
    edit_people = SelectStage(
        title='Редактирование базы людей',
        text='Выберите действие:',
        name=Stages.EDIT_PEOPLE,
    )
    add_person = SelectStage()
    define_name = InputStage(
        title='Добавить человека',
        text='Введите имя человека',
        logic=AddPersonLogic(),
        validators=(NonEmptyStringValidator(),),
    )
    remove_person = SelectStage()
    new_party = SelectStage(
        title='Новая вечеринка',
        text='Начало расчёта - добавьте людей, определите для них коэффициент и затраченные суммы',
        name=Stages.NEW_PARTY,
        logic=NewPartyLogic(),
    )
    add_participant = SelectStage(
        title='Добавить людей на вечеринку',
        text='Выберите ещё людей из сохранённого списка:',
        name=Stages.ADD_PARTICIPANT,
        logic=AddParticipantStageLogic(),
        text_factory=get_added_people,
        keyboard_builder=build_add_participant_keyboard,
    )
    define_coeff = InputStage(
        title='Укажите коэффициент для участника:',
        text='В формате дробного числа, например 1.0 (это 100%) или 0.5 (это 50%) или 2.0 (это 200%)'
             'Обычно используется 100%, 200% нужны для семей из двух человек, 50 - для тех кто мало ел',
        name=Stages.DEFINE_COEFF,
        logic=SetCoeffLogic(),
        validators=(PositiveFloatValidator(),),
    )
    define_payment = InputStage(
        title='Укажите платёж участника:',
        text='В формате дробного числа, например 123\\.56',
        name=Stages.DEFINE_PAYMENT,
        logic=SetPaymentLogic(),
        validators=(NonNegativeDecimalValidator(),),
    )
    remove_participant = SelectStage(
        title='Удаление участника вечеринки',
        text='Выберите участника, которого необходимо исключить',
        name=Stages.REMOVE_PARTICIPANT,
        logic=None,
        keyboard_builder = build_remove_participants_keyboard,
    )
    calc_result = SelectStage(
        title='Итоговый расёт',
        text='',
        name=Stages.CALC_RESULT,
        logic=None,
    )

    start.children = (main_menu, )
    main_menu.parent = start
    main_menu.children = (new_party, edit_people)
    new_party.parent = main_menu
    new_party.children = (add_participant, calc_result)
    add_participant.parent = new_party
    add_participant.children = (define_coeff, define_payment)
    define_coeff.children = (define_payment, )
    define_payment.children = (new_party, )
    calc_result.children = (main_menu, )
    edit_people.parent = main_menu
    edit_people.children = (add_person, remove_person)
    # add_person, remove_person

    menu = Menu(
        start_stage=start,
        stages=(
            start,
            main_menu,
            edit_people,
            add_person,
            define_name,
            remove_person,
            new_party,
            add_participant,
            define_coeff,
            define_payment,
            calc_result
        )
    )
    menu.html_escape()
    return menu
