import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flow.stage_data import StageData
from flow.stages import Stage

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

def log(level: int, data: StageData | None = None, stage: Stage | None = None, message: str = '...'):
    log_info = {
        'chat_id': data.chat_id,
        'stage': stage.name
    }
    logger.log(level, message, extra=log_info)

def info():
    pass

def error():
    pass

def warning():
    pass

def critical():
    pass

