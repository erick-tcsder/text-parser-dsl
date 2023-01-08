from abc import ABC, abstractmethod


class DSLType(ABC):
    @staticmethod
    @abstractmethod
    def get_dsl_name()->str:
        pass
