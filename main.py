from methods import (
    duration_curves_from_ariadne_report,
    elec_prices_ts_from_ariadne_report_1h,
    duration_curves_from_pypsa_one_node,
    elec_prices_ts_from_pypsa_one_node_1h
)

from utilities import(
    plot_daily_mean_price_timeseries
)

args = {
    "ariadne_ep_ts" : "input/electricity_prices_pypsa_DE_timeseries_ariadne_report", # electricity price time series from ariadne report
    "nc_path":"pypsa_netzwerke_one-node-pricing-lt/base_s_1__none_2045_lt.nc",
    "years": [2020,2025,2030,2035,2040,2045], # years of provided pypsa-networks from pypsa-DE-one node https://github.com/JulianGeis/pypsa-de-pricing/tree/one-node-pricing
    "output_base_dir": "outputs",  # base output dir
}

if __name__ == "__main__":

    # Ariadne

    df_1h = elec_prices_ts_from_ariadne_report_1h(args)

    plot_daily_mean_price_timeseries(
        df_1h,
        save_path="outputs/ariadne/plots",
        filename="daily_mean_electricity_prices_ariadne.png",
    )

    duration_curves_from_ariadne_report(args)

    # Pypsa-DE (One Node)

    df_1h = elec_prices_ts_from_pypsa_one_node_1h(args)

    plot_daily_mean_price_timeseries(
        df_1h,
        save_path="outputs/one_node/plots",
        filename="daily_mean_electricity_prices_one_node.png",
    )

    duration_curves_from_pypsa_one_node(args)



