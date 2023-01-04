from dataclasses import dataclass
from typing import Any, Dict
from typing_extensions import Self


@dataclass(slots=True)
class Scope:
    parent: Self | None = None
    defs: Dict[str, Any] = {}

    @property
    def isGlobal(self): return self.parent is None
