"""
dataframe.py

Pandas helper class.

All dataframe operations should live here.
"""

from typing import Any, Dict
from difflib import get_close_matches

import pandas as pd


class DataFrameTool:

    # =====================================================
    # Basic Statistics
    # =====================================================

    def mean(self, df, column):

        column = self.match_column(df, column)

        if column is None:
            raise ValueError("Column not found")

        return {
            "mean": float(df[column].mean())
        }

    def median(self, df, column):

        column = self.match_column(df, column)

        if column is None:
            raise ValueError("Column not found")

        return {
            "median": float(df[column].median())
        }

    def sum(self, df, column):

        column = self.match_column(df, column)

        if column is None:
            raise ValueError("Column not found")

        return {
            "sum": float(df[column].sum())
        }

    def count(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "count": int(len(df))
        }

    def maximum(
        self,
        df,
        column,
        result_column=None
    ):
        column = self.match_column(df, column)

        if column is None:
            raise ValueError("Column not found")

            row = df.loc[df[column].idxmax()]

        if result_column:

            result_column = self.match_column(df, result_column)

            if result_column:
                return {
                    result_column: row[result_column]
                }

        return {
            column: row[column]
        }

    def minimum(
        self,
        df,
        column,
        result_column=None
    ):
        column = self.match_column(df, column)

        if column is None:
            raise ValueError("Column not found")

        row = df.loc[df[column].idxmin()]

        if result_column:

            result_column = self.match_column(df, result_column)

            if result_column:
                return {
                    result_column: row[result_column]
                }

        return {
            column: row[column]
        }

    # =====================================================
    # DataFrame Information
    # =====================================================

    def columns(self, df: pd.DataFrame):
        return list(df.columns)

    def shape(self, df: pd.DataFrame):

        rows, cols = df.shape

        return {
            "rows": rows,
            "columns": cols
        }

    def describe(self, df: pd.DataFrame):
        return df.describe(include="all").to_dict()

    def missing_values(self, df: pd.DataFrame):
        return df.isnull().sum().to_dict()

    # =====================================================
    # Filtering
    # =====================================================

    def filter_equals(
        self,
        df: pd.DataFrame,
        column: str,
        value
    ):

        return df[df[column] == value]

    def filter_greater(
        self,
        df: pd.DataFrame,
        column: str,
        value
    ):

        return df[df[column] > value]

    def filter_less(
        self,
        df: pd.DataFrame,
        column: str,
        value
    ):

        return df[df[column] < value]

    # =====================================================
    # Sorting
    # =====================================================

    def sort(
        self,
        df: pd.DataFrame,
        column: str,
        ascending=True
    ):

        return df.sort_values(
            by=column,
            ascending=ascending
        )

    # =====================================================
    # Grouping
    # =====================================================

    def groupby_mean(
        self,
        df: pd.DataFrame,
        group_column: str,
        value_column: str
    ):

        return (
            df.groupby(group_column)[value_column]
            .mean()
            .to_dict()
        )

    def groupby_sum(
        self,
        df: pd.DataFrame,
        group_column: str,
        value_column: str
    ):

        return (
            df.groupby(group_column)[value_column]
            .sum()
            .to_dict()
        )

    # =====================================================
    # Frequency
    # =====================================================

    def value_counts(
        self,
        df: pd.DataFrame,
        column: str
    ):

        return df[column].value_counts().to_dict()

    def unique(
        self,
        df: pd.DataFrame,
        column: str
    ):

        return df[column].dropna().unique().tolist()

    # =====================================================
    # Row Selection
    # =====================================================

    def head(self, df, n=5):
        return df.head(n)

    def tail(self, df, n=5):
        return df.tail(n)

    # =====================================================
    # Max / Min Row
    # =====================================================

    def row_with_max(
        self,
        df: pd.DataFrame,
        column: str
    ):

        return df.loc[df[column].idxmax()].to_dict()

    def row_with_min(
        self,
        df: pd.DataFrame,
        column: str
    ):

        return df.loc[df[column].idxmin()].to_dict()
    
    
    def match_column(self, df, column):

        if column is None:
            return None

    # Exact match
        if column in df.columns:
            return column

    # Case-insensitive match
        for col in df.columns:
            if col.lower() == column.lower():
                return col

    # Fuzzy match
        matches = get_close_matches(
            column,
            list(df.columns),
            n=1,
            cutoff=0.5
        )

        if matches:
            return matches[0]

        return None


    def has_column(self, df, column):

        return self.match_column(df, column) is not None


    def find(
        self,
        df,
        column,
        value
    ):

        column = self.match_column(df, column)

        if column is None:
            return None

        result = df[
            df[column].astype(str).str.lower()
            ==
            str(value).lower()
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()


    def row(
        self,
        df,
        index
    ):

        return df.iloc[index].to_dict()

