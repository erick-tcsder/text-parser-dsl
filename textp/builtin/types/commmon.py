from abc import ABC, abstractmethod


class DSLType(ABC):
    @classmethod
    def get_dsl_name(cls) -> str:
        i = cls.__name__.startswith('DSL')
        return cls.__name__[3:].lower() if i else cls.__name__.lower()
