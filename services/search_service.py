"""
search_service.py

Responsible for locating datasets when the user asks a question
without providing a URL.

Current implementation:
- Detects well-known datasets.
- Returns official dataset URLs.
- Can later be extended with Gemini or web search.
"""

from typing import Optional


class SearchService:

    def __init__(self):

        self.known_datasets = {
            "mospi": "https://www.mospi.gov.in/",
            "world bank": "https://data.worldbank.org/",
            "who": "https://www.who.int/data",
            "un": "https://data.un.org/",
            "census": "https://censusindia.gov.in/",
            "india": "https://data.gov.in/"
        }

    def identify_dataset(self, question: str) -> Optional[str]:
        """
        Identify a known dataset from the user's question.
        """

        q = question.lower()

        for dataset in self.known_datasets:

            if dataset in q:
                return dataset

        return None

    def find_dataset_url(self, dataset: str) -> Optional[str]:
        """
        Returns the official dataset URL.

        Future improvements:
        - Gemini-assisted dataset search
        - Web search
        - Kaggle datasets
        - GitHub datasets
        """

        return self.known_datasets.get(dataset)

    def search(self, question: str):
        """
        Search for a dataset.

        Returns:
        {
            "dataset": str | None,
            "url": str | None
        }
        """

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
