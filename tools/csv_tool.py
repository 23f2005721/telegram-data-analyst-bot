import pandas as pd
from io import BytesIO


def read_csv(data):
    return pd.read_csv(BytesIO(data))
