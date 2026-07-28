
import pandas as pd


def normalize_text(value: object) -> str:
    """
    Convert a value to a stripped string.
    Return an empty string for missing values.
    """
    if pd.isna(value):
        return ""

    return str(value).strip()