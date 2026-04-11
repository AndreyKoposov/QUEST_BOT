from os import getenv
from typing import Optional, TypeVar, Any, Dict, Callable, Type
from pydantic import SecretStr


T = TypeVar('T')

class EnvParser():
    __parsers: Dict[Type, Callable[[str], Any]] = {
        str: str,
        int: int,
        float: float
    }

    @classmethod
    def add_parser(cls, target_type: Type[T], parser: Callable[[str], T]):
        cls.__parsers[target_type] = parser

    @classmethod
    def parse(cls, value: str, target_type: Type[T]) -> Optional[T]:
        try:
            return cls.__parsers[target_type](value)
        except (ValueError, TypeError, KeyError):
            return None

    @classmethod
    def get(cls, key: str, to_type: Type[T] = str, default: Optional[T] = None) -> T:
        value = getenv(key)
        parsed = cls.parse(value, to_type) if value else None

        if parsed is not None:
            return parsed
        if default is not None:
            return default

        raise ValueError("Error in parse .env")

def to_bool(env: str) -> bool:
    value = env.strip().lower()
    if value in ['yes', 'on', 'true', '1', 't']:
        return True
    if value in ['no', 'off', 'false', '0', 'f']:
        return False
    raise ValueError

def to_secret(env: str) -> SecretStr:
    return SecretStr(env)

EnvParser.add_parser(bool, to_bool)
EnvParser.add_parser(SecretStr, to_secret)
