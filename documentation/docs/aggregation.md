# What is an aggregation formula?

![Group 3](https://user-images.githubusercontent.com/66801011/224264480-a66d91be-fa04-4994-a719-d390d2297ff4.png)

An aggregation formula is an arithmetic formula that decides how to aggregate the result of an arbitrary amount of sub-aggregations and metrics.

Aggregating metric results is a way of approximating higher level attributes, such as maintainability or reliability. The importance of an aggregation varies depending on the user, and therefore these aggregations need fit the request of the user. Modu helps combat this by letting the user define what sub-aggregations and metrics aggregate into these higher level attributes, and potentially their importance as well. 


## Creating an aggregation formula

Let's take a closer look at how to create an aggregation formula.

Aggregation formulae exist as part of a quality model, and we define them through methods. Say for example we have a quality model **TestQM** which has an aggregation method **maintainability**, which in turn takes two metrics (_'method length'_, _'file length'_), and sums them. We would display this scenario as the following code:

```python
class TestQM(QualityModel):
    def get_desc(self) -> Dict:
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

    def maintainability(self, results: Dict) -> int | float:
        return (
            results["method_length"] + results["file_length"]
        )

model = TestQM()
```
Note that for this section, we are only looking at **maintainability**