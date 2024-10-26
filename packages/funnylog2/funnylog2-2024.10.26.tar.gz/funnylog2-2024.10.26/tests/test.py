from funnylog2 import logger
from funnylog2.config import config

config.LOG_FILE_PATH = "."

logger.info("xxx")
logger.debug("yyy")
logger.error("zzz")