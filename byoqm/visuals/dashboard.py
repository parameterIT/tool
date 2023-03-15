from collections import defaultdict
from datetime import datetime
import os
import pandas as pd
from .line import get_line
from bokeh.layouts import gridplot
from bokeh.plotting import show
from .line import get_line
import logging


class Dashboard:
    def __init__(self, start_date: datetime, end_date: datetime):
        self._start_date = start_date
        self._end_date = end_date

    def show_graphs(self):
        """
        This method is used to display the graphs chosen. At the moment, only line graphs can be chosen,
        however this can be easily expanded upon.

        The method makes use of Bokeh to generate figures, which are then added to a gridplot in the
        arrangement of an arbitrary amount of rows where each row contains two figures.
        """
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
        """
        Gets data from specified path. The path is defaulted to the output folder, but if you want to run
        BYOQM using a different path, this can be changed in the CLI.

        The name of the file depicts the date at which the tool was run. The content of the file consists
        of an arbitrary amount of metrics, together with their respective values.
        This data is collected in a dict, matching every single metric to a list containing
        tuples of dates and values.

        The data is then sorted to ensure that the dates appear in chronological order
        """
        logging.info(f"Getting data from: {path}")
        graph_data = defaultdict(list)
        for filename in os.listdir(path):
            try:
                date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d_%H-%M-%S")
                if self._start_date > date or self._end_date < date:
                    continue
                filepath = os.path.join(path, filename)
                df = pd.read_csv(filepath, header=0, skiprows=2)
                for row in df.itertuples(index=False, name=None):
                    graph_data[row[0]].append((date, row[1]))
            except:
                logging.warning(
                    f"Failed to parse file with filename: {filename} - invalid format. Check the naming convention of the file or the content of the file"
                )
        for key, v in graph_data.items():
            try:
                v.sort()
            except:
                logging.warning(f"Failed to sort data for {key} in graph_data")
        logging.info("Finished getting data")
        return graph_data
