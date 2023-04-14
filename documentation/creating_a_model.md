# Configuring a model

After creating metrics and settling on one or more aggregation formulas a quality model can be configured.

![Group 5(1)](https://user-images.githubusercontent.com/66801011/224269410-07a4eeb2-b383-4e45-b78b-f11d7adb5dd9.png)

## Configuring metrics

Configuring the metrics can be done by adding them to the model object that is to be returned from _getDesc()_.

```python
def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_length": "./metrics/method_length.py",
                "file_length": "./metrics/file_length.py",
                 ...
```

## Configuring aggregations

Configuring the aggregation formula can be done by adding the name of the aggregation to the model object that is to be returned from _getDesc()_.

```python
"aggregations": {
                "maintainability": self.maintainability,
            }
```

Look to #section4 for implementation example of aggregation formula.


## Configure the quality model
Together the two components of metrics and aggregation formulas create the model.

```python
def getDesc(self) -> Dict:
        model = {
            "metrics": {
                "method_length": "./metrics/method_length.py",
                "file_length": "./metrics/file_length.py",
            },
            "aggregations": {
                "maintainability": self.maintainability,
            },
        }
        return model
```
