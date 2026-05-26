import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 500

regions    = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Food", "Office"]
months     = pd.date_range("2024-01-01", periods=12, freq="MS")

df = pd.DataFrame({
    "date":     np.random.choice(months, n),
    "region":   np.random.choice(regions, n),
    "category": np.random.choice(categories, n),
    "revenue":  np.random.normal(15000, 4000, n).round(2),
    "units":    np.random.randint(10, 500, n),
    "cost":     np.random.normal(9000, 2000, n).round(2),
})

# Inject dirty data intentionally
df.loc[np.random.choice(n, 30, replace=False), "revenue"] = np.nan
df.loc[np.random.choice(n, 20, replace=False), "units"]   = -1
df.loc[np.random.choice(n, 15, replace=False), "cost"]    = "N/A"
df = pd.concat([df, df.sample(10)], ignore_index=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/sales_data.csv", index=False)
print(f"[01] Generated {len(df)} rows -> data/sales_data.csv")
