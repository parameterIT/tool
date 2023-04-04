class Result:
    """
    represents a result for a given metric

    a result is a collection of violations with the metric type specified
    """

    def __init__(self, metric, violations):
        self.metric = metric
        self.violations = violations

    def get_frequency(self):
        """
        returns the frequency of violations for a given metric
        """
        return len(self.violations)

    def get_violation_locations(self):
        """
        returns a list of locations defining where saved violations are found
        """
        return [violation.locations for violation in self.violations]
