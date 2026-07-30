"""
dataframe.py

Pandas helper class.

All dataframe operations should live here.
"""

from typing import Any, Dict

import pandas as pd


class DataFrameTool:

    # =====================================================
    # Basic Statistics
    # =====================================================

    def mean(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        return {
            column: float(df[column].mean())
        }

    def median(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        return {
            column: float(df[column].median())
        }

    def sum(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        return {
            column: float(df[column].sum())
        }

    def count(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "count": int(len(df))
        }

    def maximum(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        return {
            column: df[column].max()
        }

    def minimum(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        return {
            column: df[column].min()
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
