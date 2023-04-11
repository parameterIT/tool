from collections import defaultdict
from bokeh.plotting import figure
from byoqm.dashboard.figure import Figure
from bokeh.models import DatetimeTickFormatter


class Horizontal(Figure):
    def __init__(self):
        self._data: dict = defaultdict(list)

    def _get_line(self, data, key):
        x = [(value[0]) for value in data[key]]
        y = [(value[1]) for value in data[key]]
        p = figure(
            width=600,
            height=350,
            title=key,
            x_axis_type="datetime",
            x_axis_label="Date",
            y_axis_label="No. Violations",
        )
        p.line(x, y, legend_label="Progress", line_width=2)
        return p

    def get_figure(self):
        result = [self._get_line(self._data, key) for key in self._data]
        return result


fig = Horizontal()
