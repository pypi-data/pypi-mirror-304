import contextlib
import os
import subprocess

from .transformer import CodeFenceTransformer


class BashExecute(CodeFenceTransformer):
    marker = "bash-execute"

    def __init__(self, process_root):
        self.process_root = process_root

    def transform_content(self, content):
        lines = content.splitlines()
        new_content = []
        with contextlib.chdir(self.process_root):
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
        return "\n".join(new_content).rstrip("\n") + "\n"

    def finish(self, node):
        node.info_string = "sh"


class SavePythonCode(CodeFenceTransformer):
    marker = "python-code"

    def __init__(self, process_root):
        self.process_root = process_root

    def transform_content(self, content, path):
        path = path.strip()
        (self.process_root / path).write_text(content)
        return f"# {path}\n\n" + content

    def finish(self, node):
        node.info_string = "python"
