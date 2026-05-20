from bot import bot
from bot.handlers import register_handlers
from bot.log import config_logger
from db.app import Users
from flow.manager import FlowManager
from flow.menu_setup import build_menu


def main() -> None:
    Users.create_user(234391861, True)
    Users.create_user(56067311)
    Users.create_user(236383171)
    Users.create_user(787185302)
    config_logger()
    menu = build_menu()
    manager = FlowManager(bot=bot, menu=menu)
    register_handlers(bot, manager)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
