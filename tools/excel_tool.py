"""
Excel loader.
"""

from pathlib import Path
import pandas as pd


class ExcelTool:

    def load(self, path: str) -> pd.DataFrame:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_excel(path)
