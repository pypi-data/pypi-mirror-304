import pathlib
import tempfile

import mkdocs.config.config_options
import mkdocs.plugins

from .example_transformers import BashExecute, SavePythonCode
from .transformer import transform_text


class TransformMarkdownPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("max-line-length", mkdocs.config.config_options.Type(int, default=80)),
    )

    def on_page_markdown(self, markdown, page, config, files):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root_folder = pathlib.Path(tmp_dir)
            return transform_text(
                markdown,
                [
                    SavePythonCode(root_folder),
                    BashExecute(root_folder),
                ],
                config.plugins["md-transformer"].config["max-line-length"],
            )
