"""
tools/csv_tool.py

Utilities for reading and inspecting CSV files.
"""

from pathlib import Path

import pandas as pd

from services.logger import logger


class CSVTool:
    """
    CSV helper using pandas.
    """

    ENCODINGS = [
        "utf-8",
        "utf-8-sig",
        "latin-1",
        "cp1252",
    ]

    SEPARATORS = [
        ",",
        ";",
        "\t",
        "|",
    ]

    # ---------------------------------------------------------
    # Read CSV
    # ---------------------------------------------------------

    def read(self, path: str | Path) -> pd.DataFrame:
        """
        Read a CSV file using several encoding/separator combinations.
        """

        path = Path(path)

        last_error = None

        for encoding in self.ENCODINGS:

            for sep in self.SEPARATORS:

                try:

                    df = pd.read_csv(
                        path,
                        encoding=encoding,
                        sep=sep,
                        engine="python",
                    )

                    logger.log(
                        "csv_loaded",
                        path=str(path),
                        rows=len(df),
                        columns=len(df.columns),
                        encoding=encoding,
                        separator=sep,
                    )

                    return df

                except Exception as e:
                    last_error = e

        raise RuntimeError(
            f"Unable to read CSV '{path}'."
        ) from last_error

    # ---------------------------------------------------------
    # Preview
    # ---------------------------------------------------------

    def preview(
        self,
        df: pd.DataFrame,
        rows: int = 5,
    ) -> pd.DataFrame:
        """
        Return the first few rows.
        """

        return df.head(rows)

    # ---------------------------------------------------------
    # Information
    # ---------------------------------------------------------

    def info(self, df: pd.DataFrame) -> dict:
        """
        Basic dataframe metadata.
        """

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": {
                c: str(t)
                for c, t in df.dtypes.items()
            },
            "missing_values": (
                df.isna()
                .sum()
                .to_dict()
            ),
        }

    # ---------------------------------------------------------
    # Numeric Summary
    # ---------------------------------------------------------

    def describe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Statistical summary.
        """

        return df.describe(include="all")

    # ---------------------------------------------------------
    # Clean
    # ---------------------------------------------------------

    def clean(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Basic cleanup.
        """

        cleaned = df.copy()

        cleaned.columns = [
            str(c).strip()
            for c in cleaned.columns
        ]

        return cleaned

    # ---------------------------------------------------------
    # Missing Values
    # ---------------------------------------------------------

    def missing(self, df: pd.DataFrame) -> dict:
        """
        Missing values per column.
        """

        return (
            df.isna()
            .sum()
            .to_dict()
        )


csv_tool = CSVTool()
