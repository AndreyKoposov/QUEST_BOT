"""logging"""
from logging import getLogger, DEBUG, Formatter
from logging.handlers import RotatingFileHandler
from app.config import ROOT, ENV


class Logger():
    """Класс для логгирование"""
    logger = getLogger(__name__)

    @staticmethod
    def start() -> None:
        """Запускает работу логгера"""
        Logger.logger.setLevel(DEBUG)

        formatter = Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = RotatingFileHandler(
            ROOT/'logs\\app.log',
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
        if ENV.DEBUG:
            Logger.logger.info(msg)

    @staticmethod
    def error(msg):
        """Log info message"""
        Logger.logger.error(msg)
