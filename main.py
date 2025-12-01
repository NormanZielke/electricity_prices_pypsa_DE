from functions import load_electricity_price_timeseries

args = {
    "direction" : "input/electricity_prices_pypsa_DE_timeseries",
}

if __name__ == "__main__":
    df = load_electricity_price_timeseries(args["direction"])

    print("Loaded electricity price timeseries:")
    print(df.head())
