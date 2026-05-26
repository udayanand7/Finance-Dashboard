"""
05_automate.py
==============
Master pipeline script — runs all steps in order and exports
a dated Excel summary report to reports/.

Run:  python 05_automate.py
"""

import subprocess
import sys
import os
import datetime
import pandas as pd

STEPS = [
    "01_generate_data.py",
    "02_clean_data.py",
    "03_analyze.py",
    "04_visualize.py",
]


def run_pipeline():
    print("\n" + "=" * 55)
    print(f"  Financial Dashboard Pipeline")
    print(f"  Started: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 55)

    for script in STEPS:
        print(f"\n  Running {script} ...")
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True, text=True
        )
        if result.stdout:
            for line in result.stdout.strip().splitlines():
                print(f"    {line}")
        if result.returncode != 0:
            print(f"\n  ERROR in {script}:\n{result.stderr}")
            sys.exit(1)
        print(f"  ✓ {script} done")


def export_excel():
    df = pd.read_csv("data/cleaned_data.csv", parse_dates=["date"])

    monthly = (df.groupby("month")
                 .agg(Revenue=("revenue", "sum"),
                      Profit=("profit", "sum"),
                      Transactions=("revenue", "count"))
                 .reset_index())
    monthly["MoM_Growth_%"] = monthly["Revenue"].pct_change().mul(100).round(2)

    region = (df.groupby("region")
                .agg(Total_Revenue=("revenue", "sum"),
                     Avg_Margin_pct=("profit_margin", "mean"),
                     Total_Units=("units", "sum"))
                .round(2)
                .sort_values("Total_Revenue", ascending=False)
                .reset_index())

    category = (df.groupby("category")
                  .agg(Revenue=("revenue", "sum"),
                       Profit=("profit", "sum"),
                       Units=("units", "sum"))
                  .round(2)
                  .reset_index())
    category["Share_%"] = (
        category["Revenue"] / category["Revenue"].sum() * 100
    ).round(1)

    fname = f"reports/summary_{datetime.date.today()}.xlsx"
    with pd.ExcelWriter(fname, engine="openpyxl") as writer:
        monthly.to_excel(writer,  sheet_name="Monthly",  index=False)
        region.to_excel(writer,   sheet_name="Region",   index=False)
        category.to_excel(writer, sheet_name="Category", index=False)

    print(f"\n  Excel report saved: {fname}")


if __name__ == "__main__":
    run_pipeline()
    export_excel()
    print("\n" + "=" * 55)
    print("  All done! Check the reports/ folder.")
    print("=" * 55 + "\n")
