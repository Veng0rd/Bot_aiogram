from loguru import logger

logger.add(
    sink='config.cfg',
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    rotation="1 week",
    compression="zip",
    backtrace=False
)
