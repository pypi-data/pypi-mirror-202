"""Initialization file for library."""

from importlib import metadata
import os.path
import re
from typing import List

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from tabulate import tabulate
import yaml

__version__ = metadata.version(__name__)


SYNTAX = re.compile(r"^(\s*)\{data-table\s+(\S+)\}$")


class MarkdownDataTablesPreprocessor(Preprocessor):
    """Look for {data-table filename} in the markdown."""

    def __init__(self, md, config):
        super().__init__(md)
        self.base_path = config["base_path"]

    def run(self, lines: List[str]) -> List[str]:
        """Preprocess the provided Markdown source text.

        Looks for any lines that match the SYNTAX regular expression, for example:

        {data-table path/to/data.yaml}

        and replaces those lines with the output of `self.make_table()`.

        Args:
            lines: List of strings corresponding to the input file's lines.

        Returns:
            List of processed strings.
        """
        new_lines = []
        for line in lines:
            match = SYNTAX.match(line)
            if not match:
                new_lines.append(line)
                continue
            indent = match.group(1)
            filename = match.group(2)
            new_lines += self.make_table(filename, indent=indent)

        return new_lines

    def make_table(self, filename: str, indent: str = "") -> List[str]:
        """Load the given source YAML file and render its contents as a Markdown table.

        Args:
            filename: Path (absolute, or relative to self.base_path) of the YAML file to load.
            indent: Whitespace string or similar to prepend to all lines of the rendered table.

        Returns:
            List of strings defining the lines of a Markdown table.

        Raises:
            Exception: if the file does not exist, cannot be parsed as YAML, or doesn't define a table of data.
        """
        if not os.path.isabs(filename):
            filename = os.path.normpath(os.path.join(self.base_path, filename))
        with open(filename, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return [indent + line for line in tabulate(data, headers="keys", tablefmt="github").split("\n")]


class MarkdownDataTables(Extension):
    """Extension to the Markdown library providing the MarkdownDataTablesPreprocessor pre-processor class."""

    def __init__(self, **kwargs):
        self.config = {
            "base_path": [os.getcwd(), "Base path to use for locating relative filenames"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """Register the MarkdownDataTablesPreprocessor as a Markdown pre-processor class."""
        md.preprocessors.register(MarkdownDataTablesPreprocessor(md, self.getConfigs()), "data-tables", 100)


def makeExtension(**kwargs):  # pylint: disable=invalid-name
    """Function auto-called by Markdown library to discover/register extensions."""
    return MarkdownDataTables(**kwargs)
