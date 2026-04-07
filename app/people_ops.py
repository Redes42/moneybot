from dataclasses import replace

from entities.person import Person


def update_person_name(people: list[Person], person_id: int, new_name: str) -> None:
    for index, person in enumerate(people):
        if person.person_id == person_id:
            people[index] = replace(person, name=new_name)
            return
    raise ValueError("Человек не найден")


def update_person_coeff(people: list[Person], person_id: int, new_coeff: float) -> None:
    for index, person in enumerate(people):
        if person.person_id == person_id:
            people[index] = replace(person, coeff=new_coeff)
            return
    raise ValueError("Человек не найден")
