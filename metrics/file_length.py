#!/usr/bin/env python
from byoqm.metric.metric import Metric
from byoqm.source_coordinator.source_coordinator import SourceCoordinator


class FileLength(Metric):
    def __init__(self):
        self._coordinator = None

    def set_coordinator(self, coordinator: SourceCoordinator):
        self._coordinator = coordinator

    def run(self):
        count = 0
        for file in self._coordinator.src_paths:
            with open(file) as f:
                count += self._parse(f)
        return count

    def _parse(self, file):
        count = 0
        loc = sum(1 for line in file if line.rstrip())
        if loc > 250:
            count += 1
        return count


metric = FileLength()
