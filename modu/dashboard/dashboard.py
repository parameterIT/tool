from collections import defaultdict
import csv
from datetime import datetime
import importlib
import os
from pathlib import Path
import sys
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.plotting import show
import logging


class Dashboard:
    def _check_data(self, in_use_qm, target_path, filename):
        file_location = "./output/metadata/" + filename
        df = pd.read_csv(file_location, skiprows=0)
        for row in df.itertuples(index=False, name=None):
            is_right_qm = self._check_qm(row[0], in_use_qm)
            is_right_src = self._check_src_root(row[1], target_path)
            if not is_right_qm or not is_right_src:
                return False
        return True

    def _check_src_root(self, actual_src, target_src):
        if target_src == ".":
            return True
        if target_src != Path(actual_src):
            return False
        return True

    def _check_qm(self, target_qm, actual_qm):
        if target_qm != actual_qm:
            return False
        return True

    def _check_date(self, date, start_date, end_date):
        if start_date > date or end_date < date:
            return False
        return True

    # Returns bokeh objects, for input in gridplot.
    def _get_figures(self, data):
        results = {}
        figures = Path("./figures").glob("*.py")
        for figure_file in figures:
            spec = importlib.util.spec_from_file_location("figure", figure_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules["figure"] = module
            spec.loader.exec_module(module)
            module.fig._data = data
            results[figure_file] = module.fig.get_figure()
        return results

    def show_graphs(
        self,
        in_use_qm: str,
        target_path: Path,
        start_date: datetime,
        end_date: datetime,
    ):
        """
        This method is used to display the graphs chosen. At the moment, only line graphs can be chosen,
        however this can be easily expanded upon.

        The method makes use of Bokeh to generate figures, which are then added to a gridplot in the
        arrangement of an arbitrary amount of rows where each row contains two figures.
        """
        data = self._get_data(in_use_qm, target_path, start_date, end_date)
        # Need to get figure type in a dict, so that they can be passed to gridplot.
        # Format: {figure_type (str) : figure_objects (list)}
        figures = self._get_figures(data)
        plots = []
        for _, figure in figures.items():
            # placeholder variable name
            figures_to_add = [
                [figure[i], figure[i + 1]] for i in range(0, len(figure) - 1, 2)
            ]
            if len(figure) % 2 == 1:
                figures_to_add.append([figure[len(figure) - 1]])
            plots.extend(figures_to_add)
        show(gridplot(plots))

    def _get_data(
        self,
        in_use_qm: str,
        target_path: Path,
        start_date: datetime,
        end_date: datetime,
        path="./output/outcomes",
    ):
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
        logging.info(f"Getting data from: {path}")
        graph_data = defaultdict(list)
        for filename in os.listdir(path):
            if filename == ".gitkeep":
                continue
            try:
                filepath = os.path.join(path, filename)
                date = datetime.strptime(filename.split(".")[0], "%Y-%m-%d_%H-%M-%S")

                if not self._check_date(date, start_date, end_date):
                    continue
                if not self._check_data(in_use_qm, target_path, filename):
                    continue

                df = pd.read_csv(filepath, skiprows=0)
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
