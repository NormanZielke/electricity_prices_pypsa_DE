from pathlib import Path
import re
import pandas as pd


def load_electricity_price_timeseries(
    folder: str = "input/electricity_prices_pypsa_DE_timeseries"
):
    """
    Load all electricity price timeseries from the given folder and combine them
    into a single DataFrame.

    Rules:
    - CSV files in folder.
    - First column is datetime index.
    - Filename contains a 4-digit year at the end, e.g. elec_price_DE_2035.csv
    - Column name = extracted year.
    """
    folder_path = Path(folder)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    year_pattern = re.compile(r"(\d{4})(?=\.csv$)")
    series_dict = {}

    for csv_file in sorted(folder_path.glob("*.csv")):
        match = year_pattern.search(csv_file.name)
        if not match:
            # Skip files not matching naming pattern
            continue

        year = match.group(1)

        df = pd.read_csv(
            csv_file,
            index_col=0,       # first column = datetime index
            parse_dates=True
        )

        if df.shape[1] != 1:
            raise ValueError(
                f"Expected exactly one column in {csv_file}, found {df.shape[1]}."
            )

        s = df.iloc[:, 0].rename(year)
        series_dict[year] = s

    if not series_dict:
        raise RuntimeError(f"No valid CSV files found in {folder_path}")

    combined = pd.concat(series_dict.values(), axis=1)

    combined = combined.sort_index()
    combined = combined.reindex(sorted(combined.columns), axis=1)

    return combined
