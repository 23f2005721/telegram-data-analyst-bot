"""
agent/tools.py

Registry of available tools.
"""

from tools.dataframe import dataframe_tool


TOOLS = {
    "head": dataframe_tool.head,
    "tail": dataframe_tool.tail,
    "shape": dataframe_tool.shape,
    "columns": dataframe_tool.columns,

    "mean": dataframe_tool.mean,
    "median": dataframe_tool.median,
    "sum": dataframe_tool.sum,
    "maximum": dataframe_tool.maximum,
    "minimum": dataframe_tool.minimum,

    "describe": dataframe_tool.describe,
    "missing": dataframe_tool.missing,

    "unique": dataframe_tool.unique,
    "value_counts": dataframe_tool.value_counts,

    "sort": dataframe_tool.sort,
    "groupby": dataframe_tool.groupby,

    "filter_equals": dataframe_tool.filter_equals,
    "filter_greater": dataframe_tool.filter_greater,
    "filter_less": dataframe_tool.filter_less,
}
