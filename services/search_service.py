"""
search_service.py

Responsible for locating datasets when the user asks a question
without providing a URL.

Current implementation:
- Detects well-known datasets.
- Can later be extended with Gemini or web search.
"""

from typing import Optional


class SearchService:

    def __init__(self):
        self.known_datasets = {
            "mospi": None,
            "world bank": None,
            "who": None,
            "un": None,
            "census": None
        }

    def identify_dataset(self, question: str) -> Optional[str]:
        q = question.lower()

        for dataset in self.known_datasets:
            if dataset in q:
                return dataset

        return None

    def find_dataset_url(self, dataset: str) -> Optional[str]:
        """
        Placeholder.

        Future:
        - Search official website
        - Search Kaggle
        - Search GitHub
        - Ask Gemini
        """

        return self.known_datasets.get(dataset)

    def search(self, question: str):
        dataset = self.identify_dataset(question)

        if dataset is None:
            return {
                "dataset": None,
                "url": None
            }

        return {
            "dataset": dataset,
            "url": self.find_dataset_url(dataset)
        }
