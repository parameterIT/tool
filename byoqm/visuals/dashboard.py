from collections import defaultdict
import csv
from datetime import datetime
import os
from pathlib import Path
import pandas as pd
from .line import get_line
from bokeh.layouts import gridplot
from bokeh.plotting import show
from .line import get_line


class Dashboard:
    def __init__(self, start_date: datetime, end_date: datetime):
        self._start_date = start_date
        self._end_date = end_date

    def _check_data(self, filepath, in_use_qm, target_path):
        with open(filepath) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "qualitymodel" and row[1] != in_use_qm:
                    return False
                if row[0] == "src_root" and ("./" + row[1]) != target_path:
                    return False
        return True

    def _check_date(self, date, start_date, end_date):
        if start_date > date or end_date < date:
            return False
        return True

    def show_graphs(self, in_use_qm: str, targetPath: Path):
        """
        This method is used to display the graphs chosen. At the moment, only line graphs can be chosen,
        however this can be easily expanded upon.

        The method makes use of Bokeh to generate figures, which are then added to a gridplot in the
        arrangement of an arbitrary amount of rows where each row contains two figures.
        """
        data = self.get_data(in_use_qm, targetPath)
        # consider changing to broader term such as 'figures' if we plan on expanding the list to include other charts
        line_figures = [get_line(data, key) for key in data]
        gridplots = gridplot(
            [
                [line_figures[i], line_figures[i + 1]]
                for i in range(0, len(line_figures) - 1, 2)
            ]
        )
        show(gridplots)

    def get_data(self, in_use_qm: str, targetPath: Path, path="./output"):
        """
        Gets data from specified path. The path is defaulted to the output folder, but if you want to run
        BYOQM using a different path, this can be changed in the CLI.

        The name of the file depicts the date at which the tool was run. The content of the file consists
        of an arbitrary amount of metrics, together with their respective values.
        This data is collected in a dict, matching every single metric to a list containing
        tuples of dates and values.

        Graphs are only generated for the current chosen quality model and the current target path.

        The data is then sorted to ensure that the dates appear in chronological order
        """
        graph_data = defaultdict(list)
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d_%H-%M-%S")
            if not self._check_date(date, self._start_date, self._end_date):
                continue
            if not self._check_data(filepath, in_use_qm, targetPath):
                continue
            df = pd.read_csv(filepath, header=0, skiprows=2)
            for row in df.itertuples(index=False, name=None):
                graph_data[row[0]].append((date, row[1]))
        for _, v in graph_data.items():
            v.sort()
        return graph_data
