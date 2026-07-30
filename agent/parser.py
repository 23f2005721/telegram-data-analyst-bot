"""
parser.py

Parses a natural-language question into a structured task.
"""

from dataclasses import dataclass, field
from typing import Optional

import re


@dataclass
class ParsedTask:

    question: str

    url: Optional[str] = None
    dataset: Optional[str] = None

    operation: Optional[str] = None

    # target numeric column
    column: Optional[str] = None

    # output column
    result_column: Optional[str] = None

    filters: dict = field(default_factory=dict)

    requires_download: bool = False
    requires_llm: bool = False


URL_REGEX = re.compile(r"https?://\S+")


OPERATIONS = {
    "highest": "max",
    "largest": "max",
    "maximum": "max",
    "lowest": "min",
    "minimum": "min",
    "average": "mean",
    "mean": "mean",
    "median": "median",
    "sum": "sum",
    "count": "count"
}


RESULT_COLUMNS = [
    "state",
    "country",
    "city",
    "district",
    "year"
]


DATASETS = [
    "mospi",
    "world bank",
    "who",
    "census",
    "india",
    "un"
]


class Parser:

    def parse(self, question: str) -> ParsedTask:

        task = ParsedTask(question=question)

        q = question.lower()

        # ----------------------------
        # URL
        # ----------------------------

        match = URL_REGEX.search(question)

        if match:
            task.url = match.group(0)
            task.requires_download = True

        # ----------------------------
        # Operation
        # ----------------------------

        for word, op in OPERATIONS.items():

            if word in q:
                task.operation = op
                break

        # ----------------------------
        # Dataset
        # ----------------------------

        for dataset in DATASETS:

            if dataset in q:
                task.dataset = dataset
                break

        # ----------------------------
        # Guess result column
        # ----------------------------

        for rc in RESULT_COLUMNS:

            if rc in q:
                task.result_column = rc
                break

        # ----------------------------
        # Guess target column
        # ----------------------------

        words = re.findall(r"[a-zA-Z_]+", q)

        ignored = (
            set(OPERATIONS.keys())
            | set(DATASETS)
            | set(RESULT_COLUMNS)
            | {
                "which",
                "what",
                "is",
                "the",
                "of",
                "with",
                "having",
                "whose",
                "has",
                "show",
                "find"
            }
        )

        candidates = []

        for word in words:

            if word not in ignored:

                candidates.append(word)

        if candidates:
            task.column = candidates[-1]

        # ----------------------------
        # LLM fallback
        # ----------------------------

        if task.operation is None:
            task.requires_llm = True

        return task
