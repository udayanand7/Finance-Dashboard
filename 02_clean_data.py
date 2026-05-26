import pandas as pd
import numpy as np

df = pd.read_csv("data/sales_data.csv")
print(f"[02] Before cleaning: {df.shape[0]} rows, {df.shape[1]} cols")

# 1. Remove duplicates
before = len(df)
df.drop_duplicates(inplace=True)
print(f"     Duplicates removed: {before - len(df)}")

# 2. Fix data types
df["date"]    = pd.to_datetime(df["date"])
df["cost"]    = pd.to_numeric(df["cost"],    errors="coerce")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
df["units"]   = pd.to_numeric(df["units"],   errors="coerce")

# 3. Handle nulls — fill with column median
null_rev = df["revenue"].isna().sum()
null_cst = df["cost"].isna().sum()
df["revenue"].fillna(df["revenue"].median(), inplace=True)
df["cost"].fillna(df["cost"].median(), inplace=True)
print(f"     Nulls filled — revenue: {null_rev}, cost: {null_cst}")

# 4. Remove invalid rows (negative units)
invalid = (df["units"] <= 0).sum()
df = df[df["units"] > 0].copy()
print(f"     Invalid unit rows removed: {invalid}")

# 5. Outlier detection using IQR
Q1, Q3 = df["revenue"].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
df["is_outlier"] = ((df["revenue"] < lower) | (df["revenue"] > upper))
print(f"     Outliers flagged: {df['is_outlier'].sum()}")

# 6. Add derived columns
df["profit"]        = (df["revenue"] - df["cost"]).round(2)
df["profit_margin"] = (df["profit"] / df["revenue"] * 100).round(2)
df["month"]         = df["date"].dt.to_period("M").astype(str)

df.to_csv("data/cleaned_data.csv", index=False)
print(f"[02] After cleaning:  {df.shape[0]} rows, {df.shape[1]} cols -> data/cleaned_data.csv")
