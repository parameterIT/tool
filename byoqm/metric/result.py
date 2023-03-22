class Result:
    def __init__(self, metric, violations):
        self.metric = metric
        self.violations = violations

    def get_frequency(self):
        return len(self.violations)

    def get_violation_locations(self):
        return [violation.locations for violation in self.violations]

    def append(self, violation):
        self.violations.append(violation)
