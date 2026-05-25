from bot.log import error
from logic.stage_logic import (
    AddParticipantStageLogic,
    AddPersonWithCoeffLogic,
    SetCoeffLogic,
    SetPaymentLogic,
    ClearPartyLogic, SkipStageLogic, RemoveParticipantStageLogic,
    SetPersonCoeffLogic, SetPersonNameLogic, RemovePersonLogic,
    AddPersonWithoutCoeffLogic, DefineChatIdStageLogic, ChooseIsAdminStageLogic,
    DeleteUserStageLogic,
)
from flow.stages import Stages, InputStage, SelectStage
from logic.keyboards import build_add_participant_keyboard, \
    build_remove_participant_keyboard, build_remove_person_keyboard, \
    build_choices_keyboard, build_delete_user_keyboard
from logic.text_factories import get_user_name, get_participants, \
    get_full_calc_result, get_persons_list, get_short_calc_result
from flow.menu import Menu
from flow.validators import NonEmptyStringValidator, \
    NonNegativeDecimalValidator, FloatValidator, IntValidator


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
        logic=ClearPartyLogic()
    )
    admin_menu = SelectStage(
        title='Меню администратора',
        text='Выберите действие:',
        name=Stages.ADMIN_MENU,
        admin_only=True
    )
    create_user = SelectStage(
        title='Создать пользователя',
        text='',
        name=Stages.CREATE_USER,
        logic=SkipStageLogic(),
        admin_only=True
    )
    define_chat_id = InputStage(
        title='Укажите chat_id:',
        text='Формат ввода - целое число',
        name=Stages.DEFINE_CHAT_ID,
        logic=DefineChatIdStageLogic(),
        validators=(IntValidator(), ),
        admin_only=True
    )
    choose_is_admin = SelectStage(
        title='Выберите, будет ли пользователь администратором',
        text='',
        name=Stages.CHOOSE_IS_ADMIN,
        keyboard_builder=build_choices_keyboard,
        logic=ChooseIsAdminStageLogic(),
        admin_only=True,
        clear_payload_on_success=True
    )
    delete_user = SelectStage(
        title='Удалить пользователя',
        text='Выберите пользователя:',
        name=Stages.DELETE_USER,
        keyboard_builder=build_delete_user_keyboard,
        logic=DeleteUserStageLogic(),
        admin_only=True,
        clear_payload_on_success=True
    )
    help = SelectStage(
        title='Справка',
        text='Справка',
        name=Stages.HELP
    )
    edit_people = SelectStage(
        title='Редактирование базы людей',
        text='Выберите действие:',
        text_factory=get_persons_list,
        name=Stages.EDIT_PEOPLE,
    )
    add_person_with_coeff = SelectStage(
        title='Добавить человека с вводом коэффициента',
        text='Введите имя человека',
        name=Stages.ADD_PERSON_WITH_COEFF,
        logic=AddPersonWithCoeffLogic(),
    )
    add_person_wo_coeff = SelectStage(
        title='Добавить человека с коэффициентом 1.0',
        text='Введите имя человека',
        name=Stages.ADD_PERSON_WO_COEFF,
        logic=AddPersonWithoutCoeffLogic(),
    )
    define_person_name = InputStage(
        title='Добавить нового человека',
        text='Введите имя человека',
        name=Stages.DEFINE_PERSON_NAME,
        logic=SetPersonNameLogic(),
        validators=(NonEmptyStringValidator(),),
        show_back_button=True
    )
    define_person_coeff = InputStage(
        title='Добавить человека',
        text='Введите коэффицент человека',
        name=Stages.DEFINE_PERSON_COEFF,
        logic=SetPersonCoeffLogic(),
        validators=(NonEmptyStringValidator(),),
        clear_payload_on_success=True
    )
    remove_person = SelectStage(
        title='Удалить человека',
        text='Выберите человека, которого необходимо удалить из базы',
        name=Stages.REMOVE_PERSON,
        logic=RemovePersonLogic(),
        keyboard_builder=build_remove_person_keyboard,
        clear_payload_on_success=True
    )
    current_party = SelectStage(
        title='Текущая вечеринка',
        button_caption='Новая вечеринка',
        text_factory=get_participants,
        text='Добавьте ещё участников или переходите к расчёту',
        name=Stages.CURRENT_PARTY,
    )
    add_participant = SelectStage(
        title='Добавление участников на вечеринку',
        text='Выберите участников из сохранённого списка\nили отредактируйте базу людей:',
        name=Stages.ADD_PARTICIPANT,
        logic=AddParticipantStageLogic(),
        keyboard_builder=build_add_participant_keyboard,
    )
    define_participant_coeff = InputStage(
        title='Укажите коэффициент для участника:',
        text='В формате дробного числа, например 1.0 (это 100%) или 0.5 (это 50%) или 2.0 (это 200%)'
             'Обычно используется 100%, 200% нужны для семей из двух человек, 50 - для тех кто мало ел',
        name=Stages.DEFINE_PARTICIPANT_COEFF,
        logic=SetCoeffLogic(),
        validators=(NonNegativeDecimalValidator(),)
    )
    define_participant_payment = InputStage(
        title='Укажите платёж участника:',
        text='В формате дробного числа, например 123.56',
        name=Stages.DEFINE_PARTICIPANT_PAYMENT,
        logic=SetPaymentLogic(),
        validators=(NonNegativeDecimalValidator(),),
        clear_payload_on_success=True
    )
    remove_participant = SelectStage(
        title='Удаление участника вечеринки',
        text='Выберите участника, которого необходимо исключить',
        name=Stages.REMOVE_PARTICIPANT,
        logic=RemoveParticipantStageLogic(),
        keyboard_builder = build_remove_participant_keyboard,
        clear_payload_on_success=True
    )
    calc_result_full = SelectStage(
        title='Итоговый расчёт (полный):',
        text_factory=get_full_calc_result,
        name=Stages.CALC_RESULT_FULL
    )
    calc_result_short = SelectStage(
        title='Итоговый расчёт (краткий):',
        text_factory=get_short_calc_result,
        name=Stages.CALC_RESULT_SHORT
    )

    start.children = (main_menu, admin_menu, help)
    main_menu.parent = start
    main_menu.children = (current_party, edit_people)
    admin_menu.parent = start
    admin_menu.children = (create_user, delete_user)
    create_user.parent = admin_menu
    create_user.children = (define_chat_id, )
    define_chat_id.children = (choose_is_admin, )
    choose_is_admin.children = (admin_menu, )
    delete_user.parent = admin_menu
    delete_user.children = (admin_menu, )
    help.parent = start
    edit_people.parent = main_menu
    edit_people.children = (
        add_person_with_coeff,
        add_person_wo_coeff,
        remove_person
    )
    add_person_with_coeff.children = (define_person_name, )
    add_person_wo_coeff.children = (define_person_name, )
    define_person_name.parent = edit_people
    define_person_name.children = (define_person_coeff, )
    define_person_coeff.children = (add_person_wo_coeff, )
    remove_person.parent = edit_people
    remove_person.children = (edit_people, )
    current_party.parent = main_menu
    current_party.children = (
        add_participant, remove_participant, calc_result_full, calc_result_short
    )
    add_participant.parent = current_party
    add_participant.children = (define_participant_coeff, define_participant_payment)
    define_participant_coeff.children = (define_participant_payment, )
    define_participant_payment.children = (current_party, )
    remove_participant.parent = current_party
    remove_participant.children = (current_party, )
    calc_result_full.children = (main_menu, )
    calc_result_short.children = (main_menu,)

    menu = Menu(
        start_stage=start,
        stages=(
            start,
            main_menu,
            admin_menu,
            create_user,
            define_chat_id,
            choose_is_admin,
            delete_user,
            help,
            edit_people,
            add_person_with_coeff,
            add_person_wo_coeff,
            define_person_name,
            define_person_coeff,
            remove_person,
            current_party,
            add_participant,
            define_participant_coeff,
            define_participant_payment,
            remove_participant,
            calc_result_full,
            calc_result_short
        )
    )
    for stage in menu.stages:
        if not stage.default_child:
            if isinstance(stage.children, tuple):
                stage.default_child = stage.children[0]
        if isinstance(stage, SelectStage):
            if not stage.button_caption:
                stage.button_caption = stage.title
        if isinstance(stage, InputStage):
            if stage.show_back_button and stage.parent is None:
                error(message=f'Parent for {stage.name} is not configured!')
        if stage.children is not None:
            if not isinstance(stage.children, tuple):
                error(message=f'Children for {stage.name} are not tuple')
    menu.html_escape()
    return menu
