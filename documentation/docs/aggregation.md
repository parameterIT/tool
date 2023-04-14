# What is an aggregation formula?

An aggregation formula is a piece of arithmetic that decides how to aggregate the result of individual metrics. 

Aggregating metric results is a way of approximating higher level qualitative attributes, such as maintainability or reliability. However, as no such thing as a single formula for calculating such attributes exist these are often very context specific and rarely work well with a one-fits-all solution. This tool helps combat that, and lets the user define what metrics aggregate into these higher level attributes. 

![Group 3](https://user-images.githubusercontent.com/66801011/224264480-a66d91be-fa04-4994-a719-d390d2297ff4.png)

With this you can in turn decide to create multiple layers of aggregation into higher level concepts. As the output of aggregation formulas have to conform to the same output format as the metrics, one can create a tree structure of aggregating results.

![Group 6](https://user-images.githubusercontent.com/66801011/224274806-4eaa0554-321b-4d13-9095-7787fd7d9c60.png)


## Creating an aggregation formula

Let's take a closer look at how to create an aggregation formula.

In this specific example, we define the concept of maintainability as the sum of the metrics file_length and method_length. 

```python
class TestQM(QualityModel):
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

    def maintainability(self, results: Dict) -> int | float:
        return (
            results["method_length"] + results["file_length"]
        )

model = TestQM()
```