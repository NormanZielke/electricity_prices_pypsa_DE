from functions import (
    load_electricity_price_timeseries,
    compute_price_duration_curve,
)

args = {
    "direction" : "input/electricity_prices_pypsa_DE_timeseries",
}

if __name__ == "__main__":
    df = load_electricity_price_timeseries(args["direction"])

    pdc = compute_price_duration_curve(df)

    print("Loaded electricity price timeseries:")
    print(df.head())

    print("Loaded price duration curves data:")
    print(pdc.head())
