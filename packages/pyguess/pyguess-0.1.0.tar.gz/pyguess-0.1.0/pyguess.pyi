from typing import Optional

class PyCandidate:
    @property
    def street(self) -> str: ...
    @property
    def location(self) -> str: ...

def find_street(
    sens: float, street: str, loc: Optional[str | int]
) -> Optional[PyCandidate]: ...
