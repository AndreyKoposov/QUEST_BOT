# logger_setup.py
import structlog


class GameLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO и выше
        )
        self._logger = structlog.get_logger()

    def bind(self, **kwargs):
        """Привязать постоянный контекст (например, service_name)"""
        return self._logger.bind(**kwargs)

    def info(self, event: str, **kwargs):
        """Информационное сообщение"""
        self._logger.info(event, **kwargs)

    def error(self, event: str, **kwargs):
        """Сообщение об ошибке"""
        self._logger.error(event, **kwargs)

    def warning(self, event: str, **kwargs):
        """Предупреждение"""
        self._logger.warning(event, **kwargs)

    def debug(self, event: str, **kwargs):
        """Отладочное сообщение"""
        self._logger.debug(event, **kwargs)

# Глобальный экземпляр
logger = GameLogger()
