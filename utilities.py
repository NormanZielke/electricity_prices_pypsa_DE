from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("bmh")


def load_elec_price_timeseries(
    folder = "input/electricity_prices_pypsa_DE_timeseries_ariadne_report"
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


def interpolate_prices_to_hourly(df_3h):
    """
    Upsample price time series from 3-hour steps to 1-hour steps via linear interpolation.

    Assumptions:
    - df_3h.index is a DatetimeIndex (timestamps)
    - columns are years (or any identifiers) with numeric price values

    Returns:
    - df_1h with hourly frequency and linearly interpolated values per column
    """
    if not isinstance(df_3h.index, pd.DatetimeIndex):
        raise TypeError("df_3h.index must be a pandas DatetimeIndex.")

    df = df_3h.copy()

    # Ensure sorted unique timestamps
    df = df[~df.index.duplicated(keep="first")].sort_index()

    # Upsample to 1H grid and interpolate in time
    df_1h = (
        df.resample("1h").asfreq()
          .interpolate(method="time", limit_direction="both")
    )

    return df_1h


def compute_price_duration_curve(df):
    """
    Compute price-duration curves for each column in the DataFrame.

    For each column:
    - Drop NaN values.
    - Sort prices (default: descending -> high to low).
    - Return a new DataFrame where the index is the rank (1 = highest price
      if ascending=False) and columns correspond to the original columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a time-based index and one column per scenario/year.
    ascending : bool, optional
        Sort order for prices. Default is False (descending = typical PDC).

    Returns
    -------
    pd.DataFrame
        DataFrame of price-duration curves. Index = rank (1..N), columns = same
        as input.
    """

    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    sorted_series = []

    for col in df.columns:
        # Drop NaN to avoid messing up the duration
        s = df[col]#.dropna()

        if s.empty:
            raise ValueError(f"Column '{col}' contains only NaN values.")

        s_sorted = s.sort_values(ascending=False).reset_index(drop=True)
        s_sorted.name = col
        sorted_series.append(s_sorted)

    pdc_df = pd.concat(sorted_series, axis=1)

    # Make the index start at 1 to represent the rank (duration step)
    pdc_df.index = pdc_df.index + 1
    pdc_df.index.name = "rank"

    return pdc_df


def plot_price_duration_curves(
    pdc_df,
    y_min = 0,
    y_max = 400,
    save_path = "outputs/price-duration_curves",
    filename = "price_duration_curves.png",
):
    """
    Plot price-duration curves for all columns in the given DataFrame (pdc_df)
    and convert the x-axis (rank) to percentage (0–100%).
    """
    if pdc_df.empty:
        raise ValueError("Input DataFrame for plotting is empty.")

    output_path = Path(save_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # ---- Rank -> Prozent ----
    max_rank = pdc_df.index.max()
    x_percent = (pdc_df.index / max_rank) * 100  # 0–100 %

    fig, ax = plt.subplots()

    for col in pdc_df.columns:
        ax.plot(x_percent, pdc_df[col], label=str(col))

    ax.set_xlabel("Fraction of time[%]")
    ax.set_ylabel("Electricity price [€/MWh]")
    ax.set_title("Electricity price duration curves")

    if (y_min is not None) or (y_max is not None):
        ax.set_ylim(bottom=y_min, top=y_max)

    ax.set_xlim(0, 100)  # immer sauber 0–100 %
    ax.legend()
    fig.tight_layout()

    file_path = output_path / filename
    fig.savefig(file_path, dpi=300)
    plt.close(fig)

    return file_path


def plot_daily_mean_price_timeseries(
    df_prices,
    save_path="outputs/price-duration_curves",
    filename="daily_mean_electricity_prices.png",
    y_min= 0,
    y_max= 400,
    figsize=(25, 10),
):
    """
    Plot electricity price time series as daily mean values (no sorting).
    """
    import pandas as pd

    if not isinstance(df_prices.index, pd.DatetimeIndex):
        raise TypeError("df_prices.index must be a pandas DatetimeIndex.")

    df = df_prices.copy()
    df = df[~df.index.duplicated(keep="first")].sort_index()

    # Daily mean values
    df_daily = df.resample("D").mean()

    fig, ax = plt.subplots(figsize=figsize)

    df_daily.plot(ax=ax)

    ax.set_xlabel("Date")
    ax.set_ylabel("Electricity price")

    if y_min is not None or y_max is not None:
        ax.set_ylim(bottom=y_min, top=y_max)

    out_dir = Path(save_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / filename

    fig.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved daily mean price timeseries plot to {out_file}")

