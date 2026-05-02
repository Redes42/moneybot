from logic.stage_logic import (
    AddParticipantStageLogic,
    AddPersonLogic,
    SetCoeffLogic,
    SetPaymentLogic,
    NewPartyLogic,
)
from flow.stages import Stages, InputStage, SelectStage
from logic.keyboards import build_add_participant_keyboard, build_remove_participants_keyboard
from logic.text_factories import get_user_name, get_participants, get_calc_result
from flow.menu import Menu
from flow.validators import NonEmptyStringValidator, NonNegativeDecimalValidator


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
        logic=NewPartyLogic()
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
    )
    add_participant = SelectStage(
        title='Добавить людей на вечеринку',
        text='Выберите ещё людей из сохранённого списка:',
        name=Stages.ADD_PARTICIPANT,
        logic=AddParticipantStageLogic(),
        text_factory=get_participants,
        keyboard_builder=build_add_participant_keyboard,
    )
    define_coeff = InputStage(
        title='Укажите коэффициент для участника:',
        text='В формате дробного числа, например 1.0 (это 100%) или 0.5 (это 50%) или 2.0 (это 200%)'
             'Обычно используется 100%, 200% нужны для семей из двух человек, 50 - для тех кто мало ел',
        name=Stages.DEFINE_COEFF,
        logic=SetCoeffLogic(),
        validators=(NonNegativeDecimalValidator(),),
    )
    define_payment = InputStage(
        title='Укажите платёж участника:',
        text='В формате дробного числа, например 123.56',
        name=Stages.DEFINE_PAYMENT,
        logic=SetPaymentLogic(),
        validators=(NonNegativeDecimalValidator(),),
        clear_payload_on_success=True
    )
    remove_participant = SelectStage(
        title='Удаление участника вечеринки',
        text='Выберите участника, которого необходимо исключить',
        name=Stages.REMOVE_PARTICIPANT,
        logic=None,
        keyboard_builder = build_remove_participants_keyboard,
    )
    calc_result = SelectStage(
        title='Итоговый расчёт',
        text_factory=get_calc_result,
        name=Stages.CALC_RESULT,
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
    calc_result.children = (main_menu, )
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
    for stage in menu.stages:
        if not stage.default_child:
            if isinstance(stage.children, tuple):
                stage.default_child = stage.children[0]
    menu.html_escape()
    return menu
