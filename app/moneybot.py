from bot import bot
from bot.handlers import register_handlers
from flow.manager import FlowManager
from menu_setup import build_menu


def main() -> None:
    menu = build_menu()
    manager = FlowManager(bot=bot, menu=menu)
    register_handlers(bot, manager)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
