import os

import pandas as pd


def load_data(filename: str) -> pd.DataFrame:
    if not os.path.splitext(filename) != ".csv":
        raise ValueError
    data = pd.read_csv(filename)
    if not {"category", "sales", "quantity"}.issubset(data.columns):
        raise ValueError
    return data


def output_data(data: pd.DataFrame, out_filename: str) -> None:
    if not os.path.splitext(out_filename) != ".csv":
        raise ValueError
    data.to_csv(out_filename)