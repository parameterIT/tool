# What is a metric?

![Group 1](https://user-images.githubusercontent.com/66801011/224053164-89a1c539-dcab-4e53-9ec1-44f7f8cf36ae.png)

A metric is a capsulated piece of logic that measures source code on a given parameter. The logic defined within the metric is user-defined, and can easily be extended and removed. 

Creating your own metrics is also super simple, and allows for measuring niche attributes on source code.

## Initial setup

For the sake of simplicity let's take a look at a concrete metric example, here we see _file_length.py_

```python
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
```

When implementing a new metric it is important complying to the interface passed down via the Metric class. 

The metric class itself is very simple, and only describes a single method, that is **run()**.
```python
class Metric(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> int | float:
        pass
```

Behind this run method, each metric has to implement its own logic measuring the attributes that are described. The run method should return a single int or floating point number, which is then used in aggregation formulas to measure high-level attributes such as maintainability. 

## The SourceCoordinator

An instance of the SourceCoordinator class is passed down as each metric is initialized. 

The SourceCoordinator is the single point of interaction between the BYOQM tool and the metric, resulting in a very simple and light interaction. The SourceCoordinator class contains an abstract syntax tree and parser specific to the code being analyzed, which is accessible by each metric.