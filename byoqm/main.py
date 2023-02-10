from pathlib import Path
import os
from metric import Metric


path = './metrics'
metrics = []
for child in Path(path).iterdir():
    if child.is_file():
        metrics.append(Metric(child.resolve()))
        
for metric in metrics:
    print(metric.name, ':' ,metric.measure())