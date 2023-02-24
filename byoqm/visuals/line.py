from bokeh.plotting import figure

#this needs to get changed for monthly shift
def get_line(data, key):
    x = [(value[0].split("-")[2]) for value in data[key]]
    y = [(value[1]) for value in data[key]]
    p = figure(
        title=key, x_axis_label="Date", y_axis_label="Problems", width=600, height=350
    )
    p.line(x, y, legend_label="Progress", line_width=2)
    return p
