import pandas as pd


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    grouped_by_category = data.groupby("category")
    return grouped_by_category[["sales", "quantity"]].sum()