from bokeh.plotting import figure


class LineChart():
    def __init__(self, data, key):
        self.data = data
        self.key = key
    # this needs to get changed for monthly shift
    def get_line(data, key):
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
