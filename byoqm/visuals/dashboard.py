from collections import defaultdict
from datetime import datetime
import os
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.plotting import show
from visuals import line


class Dashboard:
    def show_graphs(self):
        data = self.get_data()
        # consider changing to broader term such as 'figures' if we plan on expanding the list to include other charts
        line_figures = [line.get_line(data, key) for key in data]
        gridplot = gridplot(
            [
                [line_figures[i], line_figures[i + 1]]
                for i in range(0, len(line_figures) - 1, 2)
            ]
        )
        show(gridplot)

    def get_data(self, path="./output"):
        graph_data = defaultdict(list)
        for filename in os.listdir(path):
            date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d")
            filepath = os.path.join(path, filename)
            df = pd.read_csv(filepath, header=0)
            for row in df.itertuples(index=False, name=None):
                graph_data[row[0]].append((date, row[1]))
        for _, v in graph_data.items():
            v.sort()
        return graph_data
