# data_module.py
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Dict

def load_dwellings_csv(path: str) -> pd.DataFrame:
    """
    Load the ABS 'Total dwellings commenced' CSV and return a cleaned DataFrame with:
    - Period (str), Trend (int), Seasonally adjusted (int), Date (datetime), Year (int), Quarter (str)
    """
    df = pd.read_csv(
        path,
        skiprows=1,
        names=["Period", "Trend", "Seasonally adjusted"],
        usecols=[0, 1, 2],
        dtype=str,
        engine="python",
        on_bad_lines="skip",
    )

    mask_period_like = df["Period"].str.match(r"^[A-Za-z]{3}-\d{2}$", na=False)
    df = df[mask_period_like].copy()

    for col in ["Trend", "Seasonally adjusted"]:
        df[col] = df[col].str.replace(",", "", regex=False).astype(int)

    df["Date"] = pd.to_datetime(df["Period"], format="%b-%y")
    df = df.sort_values("Date").reset_index(drop=True)
    df["Year"] = df["Date"].dt.year
    df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)

    return df

def add_growth_and_ma(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add QoQ/YoY growth (%) and 4-quarter moving averages for Trend and Seasonally adjusted.
    """
    df = df.copy()
    df["Trend_qoq_pct"] = df["Trend"].pct_change() * 100
    df["SA_qoq_pct"] = df["Seasonally adjusted"].pct_change() * 100
    df["Trend_yoy_pct"] = df["Trend"].pct_change(4) * 100
    df["SA_yoy_pct"] = df["Seasonally adjusted"].pct_change(4) * 100
    df["Trend_4q_ma"] = df["Trend"].rolling(4, min_periods=1).mean()
    df["SA_4q_ma"] = df["Seasonally adjusted"].rolling(4, min_periods=1).mean()
    return df

def summarize_series(df: pd.DataFrame) -> Dict[str, int | str]:
    """
    Return a small dict with the latest values and historical peaks.
    """
    latest = df.iloc[-1]
    return {
        "latest_period": latest["Period"],
        "latest_trend": int(latest["Trend"]),
        "latest_sa": int(latest["Seasonally adjusted"]),
        "trend_peak": int(df["Trend"].max()),
        "trend_peak_period": df.loc[df["Trend"].idxmax(), "Period"],
        "sa_peak": int(df["Seasonally adjusted"].max()),
        "sa_peak_period": df.loc[df["Seasonally adjusted"].idxmax(), "Period"],
    }

def plot_trend_vs_sa(df: pd.DataFrame, save_path: Optional[str] = None):
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Trend"], label="Trend", marker="o", linewidth=2)
    plt.plot(df["Date"], df["Seasonally adjusted"], label="Seasonally adjusted", marker="s", linewidth=2)
    plt.title("Total dwellings commenced — Trend vs Seasonally adjusted")
    plt.xlabel("Date")
    plt.ylabel("Number of dwellings")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()

def plot_sa_qoq(df: pd.DataFrame, save_path: Optional[str] = None):
    colors = ["#2b8cbe" if v >= 0 else "#de2d26" for v in df["SA_qoq_pct"].fillna(0)]
    plt.figure(figsize=(12, 5))
    plt.bar(df["Date"], df["SA_qoq_pct"], width=70, color=colors)
    plt.axhline(0, color="black", linewidth=1)
    plt.title("Quarter-over-quarter growth — Seasonally adjusted (%)")
    plt.xlabel("Date")
    plt.ylabel("Percent")
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()

def plot_sa_with_ma(df: pd.DataFrame, save_path: Optional[str] = None):
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Seasonally adjusted"], label="Seasonally adjusted", color="#888", alpha=0.6)
    plt.plot(df["Date"], df["SA_4q_ma"], label="Seasonally adjusted (4-quarter MA)", color="#08519c", linewidth=2.5)
    plt.title("Seasonally adjusted with 4-quarter moving average")
    plt.xlabel("Date")
    plt.ylabel("Number of dwellings")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
