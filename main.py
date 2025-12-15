from methods import (
    duration_curves_from_ariadne_report,
    elec_prices_ts_from_ariadne_report_1h,
    duration_curves_from_pypsa_one_node,
    elec_prices_ts_from_pypsa_one_node_1h
)

from network import load_elec_price_ts_pypsa_one_node

args = {
    "ariadne_ep_ts" : "input/electricity_prices_pypsa_DE_timeseries_ariadne_report", # electricity price time series from ariadne report
    "nc_path":"pypsa_netzwerke_one-node-pricing-lt/base_s_1__none_2045_lt.nc",
    "years": [2020,2025,2030,2035,2040,2045], # years of provided pypsa-networks from pypsa-DE-one node https://github.com/JulianGeis/pypsa-de-pricing/tree/one-node-pricing
}

if __name__ == "__main__":

    df_1h = elec_prices_ts_from_ariadne_report_1h(args)

    print(df_1h.head())

    pdc_df = duration_curves_from_ariadne_report(args)

    print(pdc_df.head())

    df_1h_pypsa = elec_prices_ts_from_pypsa_one_node_1h(args)
    print(df_1h_pypsa.head())

    pdc_pypsa = duration_curves_from_pypsa_one_node(args)
    print(pdc_pypsa.head())



