
from dataclasses import dataclass
from typing import List


@dataclass
class Statement:
    pass


@dataclass
class StatementList:
    statements: List[Statement]
