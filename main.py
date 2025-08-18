# main.py
from pathlib import Path
from data_module import (
    load_dwellings_csv,
    add_growth_and_ma,
    summarize_series,
    plot_trend_vs_sa,
    plot_sa_qoq,
    plot_sa_with_ma,
)

CSV_PATH = "Total dwellings commenced (1) (1).csv"

def main():
    df = load_dwellings_csv(CSV_PATH)
    df = add_growth_and_ma(df)

    summary = summarize_series(df)
    print(f"Latest period: {summary['latest_period']}")
    print(f"Latest Trend: {summary['latest_trend']:,}")
    print(f"Latest Seasonally adjusted: {summary['latest_sa']:,}")
    print(f"Peak Trend: {summary['trend_peak']:,} ({summary['trend_peak_period']})")
    print(f"Peak Seasonally adjusted: {summary['sa_peak']:,} ({summary['sa_peak_period']})")

    outdir = Path(".")
    plot_trend_vs_sa(df, save_path=str(outdir / "dwellings_trend_vs_sa.png"))
    plot_sa_qoq(df, save_path=str(outdir / "dwellings_sa_qoq.png"))
    plot_sa_with_ma(df, save_path=str(outdir / "dwellings_sa_moving_avg.png"))

if __name__ == "__main__":
    main()
