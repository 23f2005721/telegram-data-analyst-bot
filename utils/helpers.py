"""
Small helper functions.
"""

from pathlib import Path
import re


URL_PATTERN = re.compile(r"https?://\S+")


def extract_url(text):

    match = URL_PATTERN.search(text)

    return match.group(0) if match else None


def get_extension(path):

    return Path(path).suffix.lower()


def filename(path):

    return Path(path).name
