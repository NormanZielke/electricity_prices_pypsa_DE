from functions import (
    load_electricity_price_timeseries,
    compute_price_duration_curve,
    plot_price_duration_curves
)

args = {
    "direction" : "input/electricity_prices_pypsa_DE_timeseries",
}

if __name__ == "__main__":
    df = load_electricity_price_timeseries(args["direction"])

    pdc_df = compute_price_duration_curve(df)

    print("Loaded electricity price timeseries:")
    print(df.head())

    print(df.mean())

    print("Loaded price duration curves data:")
    print(pdc_df.head())

    plot_price_duration_curves(pdc_df)
