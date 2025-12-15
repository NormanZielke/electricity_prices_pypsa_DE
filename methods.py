
from utilities import (
    load_electricity_price_timeseries,
    compute_price_duration_curve,
    plot_price_duration_curves
)


def duration_curves_from_ariadne_report(args):

    df = load_electricity_price_timeseries(args["ariadne_ep_ts"])

    pdc_df = compute_price_duration_curve(df)

    print("Loaded electricity price timeseries:")
    print(df.head())

    print(df.mean())

    print("Loaded price duration curves data:")
    print(pdc_df.head())

    plot_price_duration_curves(pdc_df)

def duration_curves_from_pypsa_DE_one_node_pricing(self,args):

    for year in args["years"]:
        self = germany(year)
        electricity_price_series = self.network.buses_t.marginal_price["DE0 0"]
