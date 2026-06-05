import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from flow.stage_data import StageData


LOG_PATH = 'logs'

def get_log_level() -> int:
    log_level_env = os.getenv('LOG_LEVEL')
    if log_level_env == 'info':
        return logging.INFO
    elif log_level_env == 'debug':
        return logging.DEBUG
    return logging.INFO

def config_logger():
    log_dir = Path(LOG_PATH)
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger('party_money_bot')
    logger.propagate = False
    logger.setLevel(get_log_level())
    formatter = logging.Formatter(
        '%(asctime)s | '
        '%(levelname)s | '
        'chat_id=%(chat_id)s | '
        'stage=%(stage)s | '
        '%(message)s'
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    rotating_file_handler = RotatingFileHandler(
        f'{LOG_PATH}/party_money_bot.log',
        maxBytes=1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    rotating_file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(rotating_file_handler)
    return logger

logger = config_logger()

def _log(level: int, stage: Optional['Stage'] = None, data: StageData | None = None, message: str = '...'):
    if stage is None:
        stage_name = None
    else:
        stage_name = stage.name
    if data is None:
        chat_id = None
    else:
        chat_id = data.user.chat_id
    log_info = {
        'chat_id': chat_id,
        'stage': stage_name
    }
    logger.log(level, message, extra=log_info)

def debug(stage: Optional['Stage'] = None, data: StageData | None = None, message: str = '...'):
    pass
    _log(logging.DEBUG, stage, data, message)

def info(stage: Optional['Stage'] = None, data: StageData | None = None, message: str = '...'):
    _log(logging.INFO, stage, data, message)

def error(stage: Optional['Stage'] = None, data: StageData | None = None, message: str = '...'):
    _log(logging.ERROR, stage, data, message)

def warning(stage: Optional['Stage'] = None, data: StageData | None = None, message: str = '...'):
    _log(logging.WARNING, stage, data, message)

def critical(stage: Optional['Stage'] = None, data: StageData | None = None, message: str = '...'):
    _log(logging.CRITICAL, stage, data, message)

