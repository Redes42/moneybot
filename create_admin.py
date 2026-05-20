from db.app import Users
from db.db import SessionLocal


chat_id: int = int(input('Введите id пользователя (чата): '))
Users.create_user(chat_id=chat_id, is_admin=True)
print(f'Администратор с chat_id={chat_id} успешно создан!')