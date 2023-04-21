# What is a metric?

![Group 1](https://user-images.githubusercontent.com/66801011/224053164-89a1c539-dcab-4e53-9ec1-44f7f8cf36ae.png)

A metric is a capsulated piece of logic that measures source code on a given parameter. The logic defined within the metric is user-defined, and can easily be extended and removed. 

Creating your own metrics is also super simple, and allows for measuring niche attributes on source code.

## Initial setup

When implementting your own metrics, you will need to implement our metric interface, which is shown below:
```python
class Metric(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self) -> Result:
        """
        run returns a number that is the measurement of that specific metric.
        """
        pass
```

For the sake of simplicity let's take a look at a concrete metric implementation:

```python
from io import TextIOWrapper
from byoqm.metric.metric import Metric
from byoqm.metric.result import Result
from byoqm.metric.violation import Violation
from byoqm.source_repository.source_repository import SourceRepository
from metrics.util.query_translations import translate_to

class FileLength(Metric):
    def __init__(self):
        self._source_repository: SourceRepository = None

    def run(self) -> Result:
        result = Result("file length", [])
        for file in self._source_repository.src_paths:
            encoding = self._source_repository.file_encodings[file]
            with open(file, encoding=encoding) as f:
                result.violations.extend(
                    self._parse(f, self._source_repository.getAst(file), file)
                )
        return result

    def _parse(self, file, ast, path):
        """
        Finds out whether or not a file is more than 250 lines long excluding comments
        """
        violations = []
        query = self._source_repository.tree_sitter_language.query(
            f"""
            (_ [{translate_to[self._source_repository.language]["comment"]}] @comment)
            """
        )
        captures = query.captures(ast.root_node)
        count_comments = 0
        for node, _ in captures:
            count_comments += (
                node.end_point[0] - node.start_point[0]
            ) + 1  # length is zero indexed - therefore we add 1 at the end
        loc = sum(1 for line in file if line.rstrip()) - count_comments
        if loc > 250:
            violations.append(Violation("LOC", (str(path), -1, -1)))
        return violations

metric = FileLength()
```

This metric makes use of _tree-sitter_ to query out all of the commented lines, whereafter it finds out whether or not the file getting analyzed, is longer than it should. Here it is important to note that the list of violations is appended to, where each violation describes the file that violates the threshhold as well as the start and end position of the violation. Note that since file length considers the entire file a violation, both the start point and end point are set to -1.

Furthermore, it is important to note that the source repository _NEEDS_ to be introduced in the constructor of each metric as *None*. This is due to us making use of _importlib_ in runner, which needs a top level field that it can inject the source repository into. This way we simply allocate space for the object.

## The Source Repository

An instance of the SourceCoordinator class is passed down as each metric is initialized. 

The `SourceCoordinator` is the single point of interaction between the modu tool and the metric, resulting in a very simple and light interaction. The `SourceCoordinator` class contains an abstract syntax tree and parser specific to the code being analyzed, which is accessible by each metric.