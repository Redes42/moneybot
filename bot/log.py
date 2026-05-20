import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from flow.stage_data import StageData

logger = logging.getLogger('party_money_bot')
log_path = 'logs'

def config_logger():
    log_dir = Path(log_path)
    log_dir.mkdir(exist_ok=True)
    rotating_file_handler = RotatingFileHandler(
        f'{log_path}/party_money_bot.log',
        maxBytes=1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s | '
            '%(levelname)s | '
            'chat_id=%(chat_id)s | '
            'stage=%(stage)s | '
            '%(message)s'
        ),
        handlers=[
            logging.StreamHandler(),
            rotating_file_handler
        ]
    )

def _log(level: int, data: StageData | None = None, stage: Optional['Stage'] = None, message: str = '...'):
    if stage is None:
        stage_name = None
    else:
        stage_name = stage.name
    log_info = {
        'chat_id': data.chat_id,
        'stage': stage_name
    }
    logger.log(level, message, extra=log_info)

def info(data: StageData | None = None, stage: Optional['Stage'] = None, message: str = '...'):
    _log(logging.INFO, data, stage, message)

def error(data: StageData | None = None, stage: Optional['Stage'] = None, message: str = '...'):
    _log(logging.ERROR, data, stage, message)

def warning(data: StageData | None = None, stage: Optional['Stage'] = None, message: str = '...'):
    _log(logging.WARNING, data, stage, message)

def critical(data: StageData | None = None, stage: Optional['Stage'] = None, message: str = '...'):
    _log(logging.CRITICAL, data, stage, message)

