from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError

from bot.log import info
from db.db import SessionLocal
from db.models import DBUser, DBPerson
from entities.user import User
from entities.person import Person
from flow.stage_data import StageData


class Users:

    @staticmethod
    def to_user_dto(user_db: DBUser) -> User:
        return User(user_db.chat_id, is_admin=user_db.is_admin)

    @staticmethod
    def create_user(chat_id: int, is_admin: bool = False) -> User | None:
        with SessionLocal() as session:
            try:
                user_db = DBUser(chat_id=chat_id, is_admin=is_admin)
                session.add(user_db)
                session.commit()
                session.refresh(user_db)
                info(
                    message=f'Создан пользователь с chat_id={chat_id} (is_admin={is_admin})'
                )
                return Users.to_user_dto(user_db)
            except IntegrityError:
                session.rollback()
                return None

    @staticmethod
    def delete_user(chat_id: int) -> bool:
        with SessionLocal() as session:
            user = session.get(DBUser, chat_id)
            if user is None:
                return False
            session.delete(user)
            session.commit()
            return True

    @staticmethod
    def get_user(chat_id: int) -> User | None:
        with SessionLocal() as session:
            user_db = session.get(DBUser, chat_id)
            return Users.to_user_dto(user_db)

    @staticmethod
    def get_all_users() -> tuple[User, ...]:
        with SessionLocal() as session:
            users_db = select(DBUser).order_by(DBUser.chat_id)
            users_db = tuple(session.scalars(users_db))
            return tuple(Users.to_user_dto(user_db) for user_db in users_db)


class Persons:

    @staticmethod
    def to_person_dto(person_db: DBPerson) -> Person:
        return Person(
            id=person_db.id,
            name=person_db.name,
            coeff=float(person_db.coeff)
        )

    @staticmethod
    def create_person(chat_id: int, person: Person) -> Person | None:
        with SessionLocal() as session:
            try:
                person_db = DBPerson(
                    chat_id=chat_id,
                    name=person.name,
                    coeff=float(person.coeff)
                )
                session.add(person_db)
                session.commit()
                session.refresh(person_db)
                return Persons.to_person_dto(person_db)
            except IntegrityError as e:
                session.rollback()
                return None

    @staticmethod
    def get_person(person: Person) -> Person | None:
        with SessionLocal() as session:
            person_db = session.get(DBPerson, person.id)
            return Persons.to_person_dto(person_db)

    @staticmethod
    def get_persons(chat_id: int) -> tuple[Person, ...]:
        with SessionLocal() as session:
            persons_db = (
                select(DBPerson)
                .where(DBPerson.chat_id == chat_id)
                .order_by(DBPerson.id)
            )
            persons_db = list(session.scalars(persons_db))
            persons = tuple(
                Persons.to_person_dto(person_db) for person_db in persons_db
            )
            return persons

    @staticmethod
    def update_person(person: Person) -> bool:
        with SessionLocal() as session:
            person_db = session.get(DBPerson, person.id)
            if person_db is None:
                return False
            try:
                person_db.coeff = person.coeff
                person_db.name = person.name
                session.commit()
                return True
            except IntegrityError as e:
                session.rollback()
                return False

    @staticmethod
    def delete_person(person: Person) -> bool:
        with SessionLocal() as session:
            person_db = session.get(DBPerson, person.id)
            if person_db is None:
                return False
            session.delete(person_db)
            session.commit()
            return True


