from collections import defaultdict
from datetime import datetime
import os
import pandas as pd
from .line import get_line
from bokeh.layouts import gridplot
from bokeh.plotting import show
from .line import get_line


class Dashboard:
    def show_graphs(self):
        data = self.get_data()
        # consider changing to broader term such as 'figures' if we plan on expanding the list to include other charts
        line_figures = [get_line(data, key) for key in data]
        gridplots = gridplot(
            [
                [line_figures[i], line_figures[i + 1]]
                for i in range(0, len(line_figures) - 1, 2)
            ]
        )
        show(gridplots)

    def get_data(self, path="./output"):
        graph_data = defaultdict(list)
        for filename in os.listdir(path):
            date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d_%H-%M-%S")
            filepath = os.path.join(path, filename)
            df = pd.read_csv(filepath, header=0, skiprows=1)
            for row in df.itertuples(index=False, name=None):
                graph_data[row[0]].append((date, row[1]))
        for _, v in graph_data.items():
            v.sort()
        return graph_data
