from datetime import datetime
from pathlib import Path
import sys
from byoqm.runner import Runner
from byoqm.visuals.dashboard import Dashboard
import click
import logging


@click.command()
@click.argument("src_root", required=True)
@click.argument("quality_model", required=True)
@click.argument("language", required=True)
@click.option(
    "--output",
    "-o",
    type=str,
    required=False,
    help="The path to the output directory",
    default="./output",
)
@click.option(
    "--save-file",
    type=bool,
    required=False,
    help="Boolean determining whether or not a file should be saved in the output directory",
    default=True,
)
@click.option(
    "--show-graphs",
    type=bool,
    required=False,
    help="Boolean determining whether or not the dashboard should be saved",
    default=True,
)
@click.option(
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=False,
    help="The point in time that the graphs should display from",
    default=datetime(1, 1, 1),
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=False,
    help="The point in time that the graphs should display from",
    default=datetime(9999, 1, 1),
)
@click.option(
    "--verbose",
    "-v",
    type=bool,
    required=False,
    help="Extra logging",
    default=False,
)
def load(
    src_root: str,
    quality_model: str,
    language: str,
    output: str = "./output",
    save_file: bool = True,
    show_graphs: bool = True,
    start_date: datetime = datetime.min,
    end_date: datetime = datetime.max,
    verbose: bool = False,
):
    print(start_date)
    if start_date > end_date:
        logging.error(
            "Start date is greater than the end date. Please enter a valid time period."
        )
        exit(1)
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    logging.info(f"Started running")
    runner: Runner = Runner(
        quality_model, Path(src_root), Path(output), save_file, language.lower()
    )
    runner.run()
    logging.info("Finished running")
    if show_graphs:
        dashboard = Dashboard(start_date, end_date)
        dashboard.show_graphs()


if __name__ == "__main__":
    load()
