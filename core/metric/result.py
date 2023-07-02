from dataclasses import dataclass

from typing import List, Any

class Result:
    """
    represents a result for a given metric

    a result is a collection of violations with the metric type specified
    """

    def __init__(self, metric: str, violations: List, outcome: Any):
        self.metric = metric
        self.violations = violations
        self.outcome = outcome

    def get_violation_locations(self):
        """
        returns a list of locations defining where saved violations are found
        """
        return [violation.locations for violation in self.violations]
