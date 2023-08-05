import pandas as pd

def to_snake_format(sr: pd.Series) -> pd.Series:
    return (
        sr.str.strip()
        .str.lower()
        .str.replace(r" ?- ?", " ", regex=True)
        .str.replace(r"\s|_+", r" ", regex=True)
        .str.replace(r"[^A-Za-z0-9 ]+", "", regex=True)
        .str.replace(" ", "_", regex=False)
    )
