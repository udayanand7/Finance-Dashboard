import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

os.makedirs("reports", exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")

df       = pd.read_csv("data/cleaned_data.csv", parse_dates=["date"])
monthly  = pd.read_csv("data/monthly_summary.csv")
region   = pd.read_csv("data/region_summary.csv")
category = pd.read_csv("data/category_summary.csv")

# ── Chart 1: Monthly Revenue Trend ────────────────────────
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(monthly["month"], monthly["Revenue"],
        marker="o", linewidth=2.2, color="#378ADD", zorder=3)
ax.fill_between(monthly["month"], monthly["Revenue"],
                alpha=0.10, color="#378ADD")
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
ax.set_title("Monthly Revenue Trend — 2024", fontsize=13, pad=10)
ax.set_xlabel("Month"); ax.set_ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
fig.savefig("reports/01_monthly_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("[04] Chart 1 saved: 01_monthly_trend.png")

# ── Chart 2: Region Performance Bar ───────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
colors  = ["#1D9E75", "#378ADD", "#EF9F27", "#D85A30"]
region_sorted = region.sort_values("Total_Revenue")
bars = ax.barh(region_sorted["region"], region_sorted["Total_Revenue"],
               color=colors, edgecolor="none", height=0.5)
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
for bar in bars:
    w = bar.get_width()
    ax.text(w * 0.98, bar.get_y() + bar.get_height()/2,
            f"₹{w/1e6:.2f}M", va="center", ha="right",
            fontsize=10, color="white", fontweight="bold")
ax.set_title("Total Revenue by Region — 2024", fontsize=13, pad=10)
ax.set_xlabel("Revenue")
plt.tight_layout()
fig.savefig("reports/02_region_bar.png", dpi=150, bbox_inches="tight")
plt.close()
print("[04] Chart 2 saved: 02_region_bar.png")

# ── Chart 3: Category Revenue Pie ─────────────────────────
fig, ax = plt.subplots(figsize=(6, 6))
pie_colors = ["#378ADD", "#1D9E75", "#EF9F27", "#D85A30"]
wedges, texts, autotexts = ax.pie(
    category["Revenue"], labels=category["category"],
    autopct="%1.1f%%", colors=pie_colors, startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2})
for at in autotexts:
    at.set_fontsize(10); at.set_color("white"); at.set_fontweight("bold")
ax.set_title("Revenue Share by Category — 2024", fontsize=13, pad=10)
plt.tight_layout()
fig.savefig("reports/03_category_pie.png", dpi=150, bbox_inches="tight")
plt.close()
print("[04] Chart 3 saved: 03_category_pie.png")

# ── Chart 4: Profit Margin Heatmap ────────────────────────
heatmap_data = df.pivot_table(
    values="profit_margin", index="region",
    columns="category", aggfunc="mean").round(1)
fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGn",
            linewidths=0.5, ax=ax,
            cbar_kws={"label": "Profit Margin %"})
ax.set_title("Avg Profit Margin % — Region × Category", fontsize=13, pad=10)
plt.tight_layout()
fig.savefig("reports/04_margin_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("[04] Chart 4 saved: 04_margin_heatmap.png")

# ── Chart 5: Monthly Revenue vs Profit (dual bar) ─────────
fig, ax = plt.subplots(figsize=(11, 4))
x = range(len(monthly))
w = 0.4
ax.bar([i - w/2 for i in x], monthly["Revenue"],
       width=w, label="Revenue", color="#378ADD", edgecolor="none")
ax.bar([i + w/2 for i in x], monthly["Profit"],
       width=w, label="Profit",  color="#1D9E75", edgecolor="none")
ax.set_xticks(list(x)); ax.set_xticklabels(monthly["month"], rotation=45, ha="right")
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
ax.set_title("Monthly Revenue vs Profit — 2024", fontsize=13, pad=10)
ax.legend()
plt.tight_layout()
fig.savefig("reports/05_revenue_vs_profit.png", dpi=150, bbox_inches="tight")
plt.close()
print("[04] Chart 5 saved: 05_revenue_vs_profit.png")

print("[04] All 5 charts saved to reports/")
