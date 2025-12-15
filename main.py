from methods import duration_curves_from_ariadne_report

from network import load_price_timeseries_dataframe

args = {
    "ariadne_ep_ts" : "input/electricity_prices_pypsa_DE_timeseries_ariadne_report", # electricity price time series from ariadne report
    "nc_path":"pypsa_netzwerke_one-node-pricing-lt/base_s_1__none_2045_lt.nc",
    "years": [2020,2025,2030,2035,2040,2045], # years of provided pypsa-networks from pypsa-DE-one node https://github.com/JulianGeis/pypsa-de-pricing/tree/one-node-pricing
}

if __name__ == "__main__":

    duration_curves_from_ariadne_report(args)

    df_prices = load_price_timeseries_dataframe(
        years=args["years"]
    )

    print(df_prices.head())
    print(df_prices.shape)

