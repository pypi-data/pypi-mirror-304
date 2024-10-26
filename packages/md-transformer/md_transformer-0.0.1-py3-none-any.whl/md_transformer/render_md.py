import contextlib
import importlib
import inspect
import os
import pathlib
import subprocess
import sys
import tempfile

import mistletoe
from mistletoe.markdown_renderer import MarkdownRenderer

process_root = pathlib.Path(tempfile.mkdtemp())


def transform(node):
    if isinstance(node, mistletoe.block_token.CodeFence):
        process_code_fence(node)
    if isinstance(node, mistletoe.span_token.LineBreak):
        node.soft = False
    for c in getattr(node, "_children", []):
        transform(c)


def process_code_fence(node):
    match node.info_string.split():
        case ("python-code", path):
            path = path.strip()
            assert path, "invalid python-code code fence"

            node.children[0].content = f"# {path}\n\n" + node.content
            (process_root / path).write_text(node.content)
            node.info_string = "python"

        case ("bash-execute",):
            render_bash_execute(node)

        case ("include-python", path):
            include_python(node, path)


def include_python(node, path):
    parts = path.split(".")
    o = importlib.import_module(parts[0])
    for i, p in enumerate(parts[1:], 1):
        try:
            o = getattr(o, p)
        except AttributeError:
            o = importlib.import_module(".".join(parts[: i + 1]))

    node.children[0].content = inspect.getsource(o)
    node.info_string = "python"


def render_bash_execute(node):
    lines = node.content.splitlines()
    new_content = []
    with contextlib.chdir(process_root):
        for line in lines:
            new_content.append(line)
            result = subprocess.run(
                line.lstrip(" $"),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=os.environ,
            )
            new_content.extend(result.stdout.splitlines())
    node.children[0].content = "\n".join(new_content)
    node.info_string = ""


if __name__ == "__main__":
    with MarkdownRenderer(max_line_length=100) as renderer:
        with open(sys.argv[1], "r") as fh:
            doc = mistletoe.Document(fh)
        transform(doc)
        print(renderer.render(doc))
