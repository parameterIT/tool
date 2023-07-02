from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class Location:
    file: Path 
    first_line: int
    last_line: int
    
@dataclass
class Violation:
    """
    represents a single instance of an issue of a metric

    saves the type of the issue as well as the location of where it was found
    """
    metric: str
    locations: List[Location]

