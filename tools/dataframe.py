"""
tools/dataframe.py

Reusable pandas DataFrame operations.
"""

from __future__ import annotations

import pandas as pd


class DataFrameTool:
    """
    Common DataFrame operations.
    """

    # ---------------------------------------------------------
    # Basic
    # ---------------------------------------------------------

    def head(self, df: pd.DataFrame, rows: int = 5):
        return df.head(rows)

    def tail(self, df: pd.DataFrame, rows: int = 5):
        return df.tail(rows)

    def shape(self, df: pd.DataFrame):
        return df.shape

    def columns(self, df: pd.DataFrame):
        return df.columns.tolist()

    # ---------------------------------------------------------
    # Selection
    # ---------------------------------------------------------

    def select(self, df: pd.DataFrame, columns: list[str]):
        return df[columns]

    def drop(self, df: pd.DataFrame, columns: list[str]):
        return df.drop(columns=columns)

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    def filter_equals(
        self,
        df: pd.DataFrame,
        column: str,
        value,
    ):
        return df[df[column] == value]

    def filter_greater(
        self,
        df: pd.DataFrame,
        column: str,
        value,
    ):
        return df[df[column] > value]

    def filter_less(
        self,
        df: pd.DataFrame,
        column: str,
        value,
    ):
        return df[df[column] < value]

    # ---------------------------------------------------------
    # Sorting
    # ---------------------------------------------------------

    def sort(
        self,
        df: pd.DataFrame,
        column: str,
        ascending: bool = True,
    ):
        return df.sort_values(
            by=column,
            ascending=ascending,
        )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def describe(self, df: pd.DataFrame):
        return df.describe(include="all")

    def mean(self, df: pd.DataFrame, column: str):
        return df[column].mean()

    def median(self, df: pd.DataFrame, column: str):
        return df[column].median()

    def maximum(self, df: pd.DataFrame, column: str):
        return df[column].max()

    def minimum(self, df: pd.DataFrame, column: str):
        return df[column].min()

    def sum(self, df: pd.DataFrame, column: str):
        return df[column].sum()

    # ---------------------------------------------------------
    # Missing Values
    # ---------------------------------------------------------

    def missing(self, df: pd.DataFrame):
        return df.isna().sum()

    # ---------------------------------------------------------
    # Group By
    # ---------------------------------------------------------

    def groupby(
        self,
        df: pd.DataFrame,
        by: str,
        agg: dict,
    ):
        return (
            df.groupby(by)
            .agg(agg)
            .reset_index()
        )

    # ---------------------------------------------------------
    # Unique
    # ---------------------------------------------------------

    def unique(self, df: pd.DataFrame, column: str):
        return df[column].unique().tolist()

    def value_counts(
        self,
        df: pd.DataFrame,
        column: str,
    ):
        return df[column].value_counts()

    # ---------------------------------------------------------
    # Merge
    # ---------------------------------------------------------

    def merge(
        self,
        left: pd.DataFrame,
        right: pd.DataFrame,
        on: str,
        how: str = "inner",
    ):
        return pd.merge(
            left,
            right,
            on=on,
            how=how,
        )

    # ---------------------------------------------------------
    # Pivot
    # ---------------------------------------------------------

    def pivot(
        self,
        df: pd.DataFrame,
        index: str,
        columns: str,
        values: str,
    ):
        return df.pivot(
            index=index,
            columns=columns,
            values=values,
        )


dataframe_tool = DataFrameTool()
