from dataclasses import replace


from entities.person import Person

def get_person(people: list[Person], person_id: int) -> Person | None:
    for person in people:
        if person.id == person_id:
            return person
    return None

def update_person_name(people: list[Person], person_id: int, new_name: str) -> None:
    for index, person in enumerate(people):
        if person.id == person_id:
            people[index] = replace(person, name=new_name)
            return
    raise ValueError("Человек не найден")


def update_person_coeff(people: list[Person], person_id: int, new_coeff: float) -> None:
    for index, person in enumerate(people):
        if person.id == person_id:
            people[index] = replace(person, coeff=new_coeff)
            return
    raise ValueError("Человек не найден")
