from dataclasses import dataclass
from .commmon import DSLType


@dataclass(order=True, slots=True, unsafe_hash=True)
class DSLInt(DSLType):
    value: int

    @staticmethod
    def get_dsl_name() -> str:
        return 'int'
