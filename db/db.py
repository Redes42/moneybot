from entities.person import Person


def get_people(chat_id: int) -> list[Person]:
    return [
        Person(person_id=1, name='Гоша'),
        Person(person_id=2, name='Красновы', coeff=2.0),
        Person(person_id=3, name='Кирилл')
    ]

