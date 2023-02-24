import csv
import os

from bokeh.layouts import gridplot
from bokeh.plotting import show
from visuals import line


class Dashboard:
    def show_graphs(self):
        data = self.get_data()
        f = [line.get_line(data, key) for key in data]
        grid = gridplot([[f[0], f[1]], [f[2], f[3]], [f[4], f[5]]])
        show(grid)

    def sort_data_values(self, data):
        for key in data:
            data[key].sort()
        return data

    def get_data(self, path="./output"):
        graph_data = {}

        for filename in os.listdir(path):
            date = filename.split(".")[0]
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as csvfile:
                    datareader = csv.reader(csvfile)
                    for row in datareader:
                        if row[0] == "Metric":
                            continue
                        tuple = (date, int(row[1]))
                        if not row[0] in graph_data:
                            graph_data[row[0]] = [tuple]
                        else:
                            graph_data[row[0]].append(tuple)

        return self.sort_data_values(graph_data)
