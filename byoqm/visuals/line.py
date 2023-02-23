from bokeh.plotting import figure
     
def get_line(data, key):
    x = []
    y = []
    for value in data[key]:
        x.append(value[0].split('-')[2])
        y.append(value[1])
    p = figure(title=key, x_axis_label='Date', y_axis_label='Problems',width=600, height=350)
    p.line(x, y, legend_label="Progress", line_width=2)
    return p
       
        

   