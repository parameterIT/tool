from bokeh.plotting import figure


def get_line(data, key):
    newX = [(value[0].split("-")[2]) for value in data[key]]
    newY = [(value[1]) for value in data[key]]
    p = figure(
        title=key, x_axis_label="Date", y_axis_label="Problems", width=600, height=350
    )
    p.line(newX, newY, legend_label="Progress", line_width=2)
    return p
