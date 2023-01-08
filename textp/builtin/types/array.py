from abc import abstractmethod, abstractclassmethod
from dataclasses import dataclass
from typing import Dict, Type
from .commmon import DSLType


@dataclass(slots=True)
class DSLArray(DSLType):
    values: list

    @abstractclassmethod
    def get_subtype(cls) -> Type[DSLType]:
        pass

    @classmethod
    def get_dsl_name(cls) -> str:
        return cls.get_subtype().__name__+'[]'


__array_types: Dict[type, type] = {}


def get_array_type(t: Type[DSLType]) -> type:
    if t in __array_types:
        return __array_types[t]

    class BuildedArray(DSLArray):
        @classmethod
        def get_subtype(cls) -> Type[DSLType]:
            return t

    BuildedArray.__qualname__ = f'{t.__qualname__}Array'
    __array_types[t] = BuildedArray
    return BuildedArray
