import re


def extract_urls(text: str):
    return re.findall(r"https?://\S+", text)
