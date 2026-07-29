import pandas as pd


def read_tables(html):
    return pd.read_html(html)
