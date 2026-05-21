from db.app import Users

Users.create_user(787185302)
Users.create_user(234391861, True)
Users.create_user(56067311)
Users.create_user(236383171)
chat_id: int = int(input('Введите id пользователя (чата): '))
Users.create_user(chat_id=chat_id)
print(f'Пользователь с chat_id={chat_id} успешно создан!')