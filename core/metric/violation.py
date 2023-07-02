from dataclasses import dataclass
from pathlib import Path
from typing import Any, List


@dataclass
class Location:
    file: Path
    first_line: int
    last_line: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Location):
            return False
        elif other.file.resolve() != self.file.resolve():
            return False
        elif other.first_line != self.first_line:
            return False
        elif other.last_line != self.last_line:
            return False
        else:
            return True

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


@dataclass
class Violation:
    """
    represents a single instance of an issue of a metric

    saves the type of the issue as well as the location of where it was found
    """

    metric: str
    locations: List[Location]
