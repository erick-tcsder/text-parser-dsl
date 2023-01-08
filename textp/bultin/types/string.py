from dataclasses import dataclass
from .commmon import DSLType


@dataclass(order=True, slots=True, unsafe_hash=True)
class DSLString(DSLType):
    value: str
    
    @staticmethod
    def get_dsl_name() -> str:
        return 'string'