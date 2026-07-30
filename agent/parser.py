"""
parser.py

Converts natural language questions into a structured task
that executor.py can understand.

This module performs lightweight parsing first and falls back
to Gemini only when required.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class ParsedTask:
    question: str

    url: Optional[str] = None
    dataset: Optional[str] = None

    operation: Optional[str] = None
    column: Optional[str] = None
    value: Optional[str] = None

    requires_download: bool = False
    requires_llm: bool = False


URL_REGEX = re.compile(r"https?://\S+")


class Parser:

    def parse(self, question: str) -> ParsedTask:

        task = ParsedTask(question=question)

        match = URL_REGEX.search(question)

        if match:
            task.url = match.group(0)
            task.requires_download = True

        q = question.lower()

        operations = {
            "maximum": "max",
            "highest": "max",
            "largest": "max",
            "minimum": "min",
            "lowest": "min",
            "average": "mean",
            "mean": "mean",
            "median": "median",
            "sum": "sum",
            "count": "count"
        }

        for key, value in operations.items():
            if key in q:
                task.operation = value
                break

        datasets = [
            "mospi",
            "census",
            "india",
            "world bank",
            "who",
            "un"
        ]

        for ds in datasets:
            if ds in q:
                task.dataset = ds
                break

        if task.operation is None:
            task.requires_llm = True

        return task
