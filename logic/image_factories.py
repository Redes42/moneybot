from typing import Callable, Optional

from bot import bot
from flow.stage_data import StageData


type ImageFactory = Callable[[StageData], str]


def get_help_picture(data: StageData) -> str:
    return 'assets/help.jpg'

