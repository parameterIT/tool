from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum

#Placeholder data
x = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
}

data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'metric'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p = figure(height=350, title="Quality Trait", toolbar_location=None,
           tools="hover", tooltips="@metric: @value", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='metric', source=data)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

show(p)
