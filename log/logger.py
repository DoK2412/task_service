from setting import LOG_FILE_NAME
from loguru import logger


LOGGER_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {name} {function} {line} {message}"

logger.add(
        LOG_FILE_NAME,
        format=LOGGER_FORMAT,
        level='DEBUG',
        rotation='30 MB',
        compression='zip',
        colorize=True
    )
