from pathlib import Path

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

    out_dir = Path(args["output_base_dir"]) / "ariadne"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "elec_prices_ariadne.csv"
    df_1h.to_csv(csv_path)

    print(f"Saved Ariadne hourly electricity prices to {csv_path}")

    return df_1h


def duration_curves_from_ariadne_report(args):

    df_1h = elec_prices_ts_from_ariadne_report_1h(args)

    pdc_df = compute_price_duration_curve(df_1h)

    out_dir = Path(args["output_base_dir"]) / "ariadne"
    png_path = out_dir / "plots"
    filename = "price_duration_curves_ariadne.png"

    plot_price_duration_curves(pdc_df, save_path=png_path, filename=filename)

    print(f"Saved Ariadne price duration curves plot to {png_path}")

    return


def elec_prices_ts_from_pypsa_one_node_1h(args):
    """
    Load electricity price time series from PyPSA-DE one-node networks (3h)
    and interpolate to 1h.
    """
    df_3h = load_elec_price_ts_pypsa_one_node(years=args["years"])
    df_1h = interpolate_prices_to_hourly(df_3h)

    out_dir = Path(args["output_base_dir"]) / "one_node"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "elec_prices_one_node.csv"
    df_1h.to_csv(csv_path)

    print(f"Saved PyPSA one-node hourly electricity prices to {csv_path}")

    return df_1h


def duration_curves_from_pypsa_one_node(args):
    """
    Compute price-duration curves from PyPSA-DE one-node networks (interpolated to 1h).
    """
    df_1h = elec_prices_ts_from_pypsa_one_node_1h(args)

    pdc_df = compute_price_duration_curve(df_1h)

    out_dir = Path(args["output_base_dir"]) / "one_node"
    png_path = out_dir / "plots"
    filename = "price_duration_curves_one_node.png"

    plot_price_duration_curves(pdc_df, save_path=png_path, filename=filename)

    print(f"Saved PyPSA one-node price duration curves plot to {png_path}")

    return
