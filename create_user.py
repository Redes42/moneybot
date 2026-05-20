from db.app import Users


chat_id: int = int(input('Введите id пользователя (чата): '))
Users.create_user(chat_id=chat_id)
print(f'Пользователь с chat_id={chat_id} успешно создан!')