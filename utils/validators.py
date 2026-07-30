"""
Validation helpers.
"""

from pathlib import Path

from utils.constants import SUPPORTED_EXTENSIONS


def is_supported_file(path):

    return Path(path).suffix.lower() in SUPPORTED_EXTENSIONS


def validate_dataframe(df):

    return df is not None and not df.empty


def validate_json(obj):

    return isinstance(obj, dict)
