from telebot import types, TeleBot

from bot.safe_sender import send_safe_message
from db.app import Users
from flow.manager import FlowManager
from flow.stages import Stages


def register_handlers(bot: TeleBot, manager: FlowManager) -> None:
    @bot.message_handler(commands=[Stages.START])
    def start_handler(message):
        chat_id = message.chat.id
        if not manager.is_allowed_user(chat_id):
            return
        try:
            session = manager.get_session(chat_id)
            manager.open_stage(session, manager.menu.start_stage)
        except ValueError as exc:
            send_safe_message(chat_id, str(exc))
        except Exception:
            send_safe_message(chat_id, 'Произошла внутренняя ошибка.')
            raise

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id, '')
        try:
            manager.handle_callback(chat_id, call.data)
        except ValueError as exc:
            send_safe_message(chat_id, str(exc))
        except Exception:
            send_safe_message(chat_id, 'Произошла внутренняя ошибка.')
            raise

    @bot.message_handler()
    def message_handler(message: types.Message):
        chat_id = message.chat.id
        try:
            manager.handle_message(message)
        except ValueError as exc:
            send_safe_message(chat_id, str(exc))
        except Exception:
            send_safe_message(chat_id, 'Произошла внутренняя ошибка.')
            raise
