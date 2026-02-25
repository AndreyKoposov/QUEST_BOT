"""logging"""
from logging import getLogger, DEBUG, Formatter
from logging.handlers import RotatingFileHandler


class Logger():
    """Класс для логгирование"""
    logger = getLogger(__name__)

    @staticmethod
    def start(path: str) -> None:
        """Запускает работу логгера"""
        Logger.logger.setLevel(DEBUG)

        formatter = Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = RotatingFileHandler(
            path + 'app\\logs\\app.log',
            maxBytes=1024*1024,
            encoding='utf-8'
        )
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(formatter)

        Logger.logger.addHandler(file_handler)
        Logger.logger.info('Started')

    @staticmethod
    def info(msg):
        """Log info message"""
        Logger.logger.info(msg)

    @staticmethod
    def error(msg):
        """Log info message"""
        Logger.logger.error(msg)
