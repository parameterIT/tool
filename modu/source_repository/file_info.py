from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileInfo:
    """
    FileInfo collects the information a SourceRepository makes available for each file
    """

    file_path: Path
    encoding: str
    language: str
