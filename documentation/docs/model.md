# Configuring a model

After creating metrics and settling on one or more aggregation formulas a quality model can be configured.

![Group 5(1)](https://user-images.githubusercontent.com/66801011/224269410-07a4eeb2-b383-4e45-b78b-f11d7adb5dd9.png)

All new quality models will need to implement the abstract class **quality_model** as displayed below:
```python
from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path


class QualityModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getDesc(self) -> Dict:
        """
        getDesc returns a dictionary describing the quality model.

        The first level of the dictionary should be two keys:
        - metrics
        - aggregations

        The value of metrics should be a nested dictionary where key-value pairs are
        metric name-path to metric executable pairs.

        The value of aggregations should be a nested dictionary where key-value pairs
        are aggregation name-aggregation function reference pairs
        """
        pass
```

## Configuring metrics

Configuring the metrics can be done by adding them to the **Dict** object returned from _getDesc()_.

```python
def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_length": "./metrics/method_length.py",
                "file_length": "./metrics/file_length.py",
                 ...
            }
        }
```
Here we aim to to map each metric to their respective paths, so the **runner** can run the metrcis.

## Configuring aggregations

Configuring the aggregation formula can be done by adding the name of the aggregation to the model object that is to be returned from _getDesc()_.

```python
"aggregations": {
                "maintainability": self.maintainability,
            }
```

As explained in the previous section, our goal here is to implement our aggregation formulae as methods and then mapping them to their respective names. 

