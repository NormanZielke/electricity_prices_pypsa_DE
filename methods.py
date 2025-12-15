
from utilities import (
    load_elec_price_timeseries,
    interpolate_prices_to_hourly,
    compute_price_duration_curve,
    plot_price_duration_curves
)


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
