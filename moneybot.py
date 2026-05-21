from bot import bot
from bot.handlers import register_handlers
from bot.log import config_logger
import threading

from flow.fake_server import run_health_server
from flow.manager import FlowManager
from flow.menu_setup import build_menu


def main() -> None:
    threading.Thread(target=run_health_server, daemon=True).start()
    config_logger()
    menu = build_menu()
    manager = FlowManager(bot=bot, menu=menu)
    register_handlers(bot, manager)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
