from abc import ABC, abstractmethod
import subprocess
from pathlib import Path


class Metric:
    def __init__(self, path: Path):
        self.path = path.resolve()
        self.name = path.name

    def measure(self) -> int | float:
        process = subprocess.run([self.path], stdout=subprocess.PIPE)
        result = process.stdout.decode("utf-8").strip()
        return result

    def to_string(self):
        return f"{self.name}: {self.path}\n"
