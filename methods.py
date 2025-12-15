
from utilities import (
    load_elec_price_timeseries,
    interpolate_prices_to_hourly,
    compute_price_duration_curve,
    plot_price_duration_curves
)

from network import load_elec_price_ts_pypsa_one_node


def elec_prices_ts_from_ariadne_report_1h(args):

    df_3h = load_elec_price_timeseries(args["ariadne_ep_ts"])

    df_1h = interpolate_prices_to_hourly(df_3h)

    return df_1h


def duration_curves_from_ariadne_report(args):

    df_1h = elec_prices_ts_from_ariadne_report_1h(args)

    pdc_df = compute_price_duration_curve(df_1h)

    print("Loaded electricity price timeseries:")
    print(df_1h.head())

    print(df_1h.mean())

    print("Loaded price duration curves data:")
    print(pdc_df.head())

    plot_price_duration_curves(pdc_df)

    return pdc_df


def elec_prices_ts_from_pypsa_one_node_1h(args):
    """
    Load electricity price time series from PyPSA-DE one-node networks (3h)
    and interpolate to 1h.
    """
    df_3h = load_elec_price_ts_pypsa_one_node(years=args["years"])
    df_1h = interpolate_prices_to_hourly(df_3h)
    return df_1h


def duration_curves_from_pypsa_one_node(args):
    """
    Compute price-duration curves from PyPSA-DE one-node networks (interpolated to 1h).
    """
    df_1h = elec_prices_ts_from_pypsa_one_node_1h(args)

    pdc_df = compute_price_duration_curve(df_1h)

    print("Loaded PyPSA one-node electricity price timeseries (1h):")

    print("Loaded price duration curves data (PyPSA one-node):")

    plot_price_duration_curves(pdc_df)

    return pdc_df
