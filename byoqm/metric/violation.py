class Violation:
    """
    represents a single instance of an issue of a metric

    saves the type of the issue as well as the location of where it was found
    """
    def __init__(self, metric, locations):
        self.metric = metric
        self.locations = locations
