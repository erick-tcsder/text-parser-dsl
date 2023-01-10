from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DSLType(ABC):
    value: Any

    @classmethod
    def get_dsl_name(cls) -> str:
        i = cls.__name__.startswith('DSL')
        return cls.__name__[3:].lower() if i else cls.__name__.lower()
