import pypsa
import pandas as pd
from pathlib import Path


class germany_network:

    def __init__(self,year):
        self.year = year
        self.network = pypsa.Network(f"input/pypsa_netzwerke_one-node-pricing-lt/base_s_1__none_{self.year}_lt.nc")


    def electricity_price_series(self):
            s = self.network.buses_t.marginal_price["DE0 0"].copy()
            s.name = str(self.year)
            return s


def load_elec_price_ts_pypsa_one_node(
    years
):
    """
    Load marginal price time series from multiple PyPSA networks into one DataFrame.

    Returns
    -------
    df: pd.DataFrame
        Index = timestamps, columns = years (as strings).
    """

    series_list = []
    for y in years:
        de = germany_network(year=y)
        series_list.append(de.electricity_price_series())

    df = pd.concat(series_list, axis=1)

    # Safety: ensure columns are ordered like input years
    df = df[[str(y) for y in years]]

    # Optional: enforce datetime index (PyPSA usually already provides it)
    df.index = pd.to_datetime(df.index)

    return df