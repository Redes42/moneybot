from enum import StrEnum

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
