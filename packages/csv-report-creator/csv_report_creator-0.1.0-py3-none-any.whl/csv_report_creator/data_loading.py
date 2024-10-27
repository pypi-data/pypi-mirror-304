import pandas as pd
import os


def load_data(filename: str) -> pd.DataFrame | None:
    if os.path.splitext(filename)[1] != ".csv":
        return None
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        return None
    return df


def write_data(data: pd.Series, filename: str) -> None:
    output_string = get_output_string(data)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output_string)


def get_output_string(data: pd.Series) -> str:
    return "\n".join([f"{category}: {total} руб." for category, total in data.items()])
