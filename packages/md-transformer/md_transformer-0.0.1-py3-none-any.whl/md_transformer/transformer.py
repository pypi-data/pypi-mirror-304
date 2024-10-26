import abc
import pathlib
import re
import shlex

import mistletoe
from mistletoe.block_token import CodeFence
from mistletoe.markdown_renderer import MarkdownRenderer
from mistletoe.span_token import LineBreak, RawText


def transform(fh_in, fh_out, transformers, max_line_length=100):
    with MarkdownRenderer(max_line_length=max_line_length) as renderer:
        text = expand_includes(fh_in.read())
        doc = mistletoe.Document(text)
        _transform(doc, list(transformers) + [FixLinebreak()])
        print(renderer.render(doc), file=fh_out)


def transform_text(text, transformers, max_line_length=100):
    with MarkdownRenderer(max_line_length=max_line_length) as renderer:
        text = expand_includes(text)
        doc = mistletoe.Document(text)
        _transform(doc, list(transformers) + [FixLinebreak()])
        return renderer.render(doc)


def expand_includes(text):
    def load(match):
        return pathlib.Path(match.group(1).strip()).read_text()

    return re.sub(r"{% *include (.+) *%}", load, text)


class MarkdownTransformer(abc.ABC):
    token_type = None

    @abc.abstractmethod
    def transform(self, node): ...


class FixLinebreak(MarkdownTransformer):
    token_type = LineBreak

    def transform(self, node):
        node.soft = False


class CodeFenceTransformer(MarkdownTransformer):
    token_type = CodeFence
    marker = None

    def transform(self, node):
        marker, *args = node.info_string.split()
        if marker != self.marker:
            return
        node.children[0].content = self.transform_content(node.content, *args)
        self.finish(node)

    def finish(self, node):
        pass


class MacroExpander(MarkdownTransformer):
    token_type = RawText

    def transform(self, node):
        node.content = re.sub(
            rf"{{% *{self.command} (.*)%}}",
            lambda m: self.expand(*shlex.split(m.group(1).strip())),
            node.content,
        )

    @abc.abstractmethod
    def expand(self, *args):
        pass


def _transform(node, transformers):
    for transformer in transformers:
        if transformer.token_type is not None:
            if not isinstance(node, transformer.token_type):
                continue
        transformer.transform(node)

    for child in node.children or []:
        _transform(child, transformers)
