from bot import bot
from bot.handlers import register_handlers
from bot.log import info
import threading

from flow.fake_server import run_health_server
from flow.manager import FlowManager
from flow.menu_setup import build_menu
from flow.stages import Stages


def main() -> None:
    threading.Thread(target=run_health_server, daemon=True).start()
    info(stage=Stages.START, message='Bot started')
    menu = build_menu()
    manager = FlowManager(bot=bot, menu=menu)
    register_handlers(bot, manager)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
