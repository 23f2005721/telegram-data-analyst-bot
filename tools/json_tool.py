"""
JSON loader.
"""

from pathlib import Path
import pandas as pd


class JSONTool:

    def load(self, path: str):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_json(path)
