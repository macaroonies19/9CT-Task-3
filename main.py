from __future__ import annotations
from pathlib import Path
import sys

from data_module import (
    load_dwellings_csv,
    add_growth_and_ma,
    summarize_series,
    plot_trend_vs_sa,
    plot_sa_qoq,
    plot_sa_with_ma,
)

CSV_PATH = Path(__file__).with_name("Total dwellings commenced (1) (1).csv")
OUTDIR = Path("figures")

def print_header():
    print("=" * 64)
    print("Dwelling Data — Terminal Explorer")
    print("=" * 64)

def print_menu():
    print("\nChoose an option:")
    print("  1) Show latest summary")
    print("  2) Show peaks and troughs")
    print("  3) Generate charts (PNG files)")
    print("  4) Export cleaned dataset with metrics (CSV)")
    print("  5) Exit")

def ensure_data():
    if not CSV_PATH.exists():
        print(f"\nERROR: CSV not found at: {CSV_PATH.name}")
        sys.exit(1)
    df = load_dwellings_csv(str(CSV_PATH))
    df = add_growth_and_ma(df)
    return df

def show_latest_summary(df):
    s = summarize_series(df)
    print("\nLatest summary")
    print("-" * 64)
    print(f"Period: {s['latest_period']}")
    print(f"Trend: {s['latest_trend']:,}")
    print(f"Seasonally adjusted: {s['latest_sa']:,}")
    if s['trend_qoq_pct'] is not None:
        print(f"QoQ (Trend): {s['trend_qoq_pct']:.2f}%")
    if s['sa_qoq_pct'] is not None:
        print(f"QoQ (Seasonally adjusted): {s['sa_qoq_pct']:.2f}%")
    if s['trend_yoy_pct'] is not None:
        print(f"YoY (Trend): {s['trend_yoy_pct']:.2f}%")
    if s['sa_yoy_pct'] is not None:
        print(f"YoY (Seasonally adjusted): {s['sa_yoy_pct']:.2f}%")

def show_extremes(df):
    s = summarize_series(df)
    print("\nPeaks and troughs")
    print("-" * 64)
    print(f"Peak Trend: {s['trend_peak']:,} ({s['trend_peak_period']})")
    print(f"Trough Trend: {s['trend_trough']:,} ({s['trend_trough_period']})")
    print(f"Peak Seasonally adjusted: {s['sa_peak']:,} ({s['sa_peak_period']})")
    print(f"Trough Seasonally adjusted: {s['sa_trough']:,} ({s['sa_trough_period']})")

def generate_charts(df):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    plot_trend_vs_sa(df, save_path=str(OUTDIR / "dwellings_trend_vs_sa.png"))
    plot_sa_qoq(df, save_path=str(OUTDIR / "dwellings_sa_qoq.png"))
    plot_sa_with_ma(df, save_path=str(OUTDIR / "dwellings_sa_moving_avg.png"))
    print(f"\nSaved charts to: {OUTDIR.resolve()}")

def export_cleaned(df):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out_csv = OUTDIR / "dwellings_clean_with_metrics.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nExported cleaned dataset to: {out_csv.resolve()}")
