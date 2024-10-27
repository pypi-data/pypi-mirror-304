import pandas as pd


def get_totals_by_categories(data: pd.DataFrame) -> pd.Series | None:
    required_columns = {"category", "amount"}
    if not required_columns.issubset(data.columns):
        return None
    grouped_by_categories = data.groupby("category")
    return grouped_by_categories["amount"].sum()
