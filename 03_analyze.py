import pandas as pd

df = pd.read_csv("data/cleaned_data.csv", parse_dates=["date"])

# Monthly revenue trend
monthly = (df.groupby("month")
             .agg(Revenue=("revenue", "sum"),
                  Profit=("profit", "sum"),
                  Transactions=("revenue", "count"))
             .reset_index())
monthly["MoM_Growth_%"] = monthly["Revenue"].pct_change().mul(100).round(2)

# Region performance
region = (df.groupby("region")
            .agg(Total_Revenue=("revenue", "sum"),
                 Avg_Margin_pct=("profit_margin", "mean"),
                 Total_Units=("units", "sum"))
            .round(2)
            .sort_values("Total_Revenue", ascending=False))

# Category breakdown
category = (df.groupby("category")
              .agg(Revenue=("revenue", "sum"),
                   Profit=("profit", "sum"),
                   Units=("units", "sum"))
              .round(2))
category["Share_%"] = (category["Revenue"] / category["Revenue"].sum() * 100).round(1)

# Save analysis outputs
monthly.to_csv("data/monthly_summary.csv",   index=False)
region.to_csv("data/region_summary.csv",     index=True)
category.to_csv("data/category_summary.csv", index=True)

print("[03] Analysis complete. Summaries saved.")
print("\n--- Monthly Trend (last 3 months) ---")
print(monthly.tail(3).to_string(index=False))
print("\n--- Region Performance ---")
print(region.to_string())
print("\n--- Category Share ---")
print(category.to_string())
