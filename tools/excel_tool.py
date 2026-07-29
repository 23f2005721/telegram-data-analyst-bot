import pandas as pd
from io import BytesIO


def read_excel(data):
    return pd.read_excel(BytesIO(data))
