from typing import Any, TypeVar, Generic, Type


T = TypeVar('T')

class Wrapper(Generic[T]):
    def __init__(self, cls: Type[T]):
        self.__cls = cls

    def to_json(self, obj: T) -> dict:
        json_obj = {}
        for attr, value in obj.__dict__.items():
            json_obj[attr] = value
        return json_obj

    def from_json(self, json_obj: dict[str, Any]) -> T:
        obj = self.__cls()
        for attr in obj.__dict__.keys():
            setattr(obj, attr, json_obj[attr])
        return obj

    @property
    def name(self) -> str:
        return getattr(self.__cls, '__colname__')

    @property
    def key(self) -> str:
        return getattr(self.__cls, '__pk__')
