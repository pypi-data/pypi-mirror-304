import pathlib
import sys
import tempfile

import click

from .example_transformers import BashExecute, SavePythonCode
from .transformer import transform


@click.command()
@click.option("--max-line-length", default=100, help="maximum line length")
@click.argument("in_file", type=click.File(), nargs=1)
def main(in_file, max_line_length):
    with tempfile.TemporaryDirectory() as tmp_dir:
        root_folder = pathlib.Path(tmp_dir)
        transform(
            in_file,
            sys.stdout,
            [
                SavePythonCode(root_folder),
                BashExecute(root_folder),
            ],
            max_line_length,
        )


if __name__ == "__main__":
    main()
