from datetime import datetime
from pathlib import Path
from core.runner import Runner
from core.dashboard.dashboard import Dashboard
import click
import logging

from core.writer import Writer


@click.command()
@click.argument("src_root", required=True)
@click.argument("quality_model", required=True)
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
    output: str = "./output",
    save_file: bool = True,
    show_graphs: bool = True,
    start_date: datetime = datetime.min,
    end_date: datetime = datetime.max,
    verbose: bool = False,
):
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

    runner: Runner = Runner(quality_model, Path(src_root))
    results = runner.run()
    writer: Writer = Writer()
    if save_file:
        writer.gen_output_paths_if_not_exists(output)
        writer.write_to_csv(results, output, quality_model, src_root)
    if show_graphs:
        dashboard = Dashboard()
        dashboard.show_graphs(quality_model, Path(src_root), start_date, end_date)


if __name__ == "__main__":
    load()
