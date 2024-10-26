import os
import time
from loguru import logger
from .constant import log_level, log_dir

log_path_app = os.path.join(log_dir, f'app.{time.strftime("%Y-%m-%d")}.log')
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <bold><level>{level}</level></bold>:<magenta>{message}</magenta>",
    colorize=True,
    level=log_level,
    backtrace=False,
    diagnose=False,
)
logger.add(log_path_app, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level=log_level)
