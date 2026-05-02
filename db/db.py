from entities.person import Person


def get_people(chat_id: int) -> list[Person]:
    return [
        Person(id=1, name='Гоша'),
        Person(id=2, name='Красновы', coeff=2.0),
        Person(id=3, name='Кирилл'),
        Person(id=4, name='Инфин'),
    ]

