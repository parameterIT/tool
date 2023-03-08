from pathlib import Path
import sys
from byoqm.runner import Runner
from byoqm.visuals.dashboard import Dashboard
import click


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
def load(
    src_root: str,
    quality_model: str,
    output: str = "./output",
    save_file: bool = True,
    show_graphs: bool = True,
):
    runner: Runner = Runner(quality_model, Path(src_root), Path(output), save_file)
    runner.run()
    if show_graphs:
        dashboard = Dashboard()
        dashboard.show_graphs()


if __name__ == "__main__":
    load()
