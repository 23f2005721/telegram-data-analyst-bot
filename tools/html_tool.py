"""
Loads HTML tables into a DataFrame.
"""

from pathlib import Path
import pandas as pd


class HTMLTool:

    def load(self, path: str):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        tables = pd.read_html(path)

        if not tables:
            raise ValueError("No tables found")

        return tables[0]
