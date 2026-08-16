# Supply Chain Inventory Optimization
End-to-end inventory analysis using **Python, SQL, Excel, and Power BI** — applying ABC Analysis, EOQ, Safety Stock, and Reorder Point to the DataCo Smart Supply Chain dataset (Kaggle).

## Problem
Identify which products deserve the tightest inventory control, how much to order, and when to reorder — reducing holding costs while avoiding stockouts.

## Dataset
- Source: [DataCo Smart Supply Chain Dataset](https://www.kaggle.com/) (Kaggle)
- 180,519 rows, 118 unique products, Jan 2015 – Jan 2018
- Filtered to `COMPLETE`/`CLOSED` orders only, to represent realized demand

## Key Assumptions
| Assumption | Value |
|---|---|
| Ordering cost | $50/order (flat) |
| Holding cost % (A / B / C) | 25% / 20% / 15% of unit price |
| Lead time | Proxied by `Days for shipping (real)` (no supplier lead-time field in source data) |
| Service level (A / B / C) | 98% / 95% / 90% (Z = 2.05 / 1.65 / 1.28) |
| Annual demand | 3-year total quantity ÷ 3 |

**Formulas:**
```
EOQ  = sqrt(2 × Annual Demand × Ordering Cost / Holding Cost)
SS   = Z × Std Dev(Daily Demand) × sqrt(Lead Time)
ROP  = (Avg Daily Demand × Lead Time) + SS
```

## Pipeline
**Python** → cleaned data, computed ABC class, EOQ, Safety Stock, ROP per product → exported to CSV
**MySQL** → loaded `products` (118 rows) and `transactions` tables, joined for KPI queries
**Excel** → Pivot Tables + Pareto chart to validate SQL/Python results
**Power BI** → 4-page interactive dashboard connected live to MySQL

## Dashboard
- **Overview:** KPI cards, revenue by ABC class, top 10 products, decomposition tree
- **ABC Analysis:** Pareto chart, SKU%/Revenue%/Quantity% comparison by class
- **Inventory Health:** Safety Stock risk table, demand variability scatter, lead time by class
- **Ordering & Regional:** orders/year by product, revenue & shipping delay by region

## Key Insights
*(fill in from your final numbers)*
- Class A = **[X]%** of products generating **[Y]%** of revenue
- **[N]** products flagged for reorder risk (high Safety Stock relative to ROP)
- [Add 1–2 more from your dashboard]

## Limitations
No live inventory snapshot in source data — stock levels/reorder alerts are simulated. Ordering/holding costs are assumptions, not actuals. Lead time is a shipping-time proxy, not true supplier lead time.

## Repo Structure
```
data/       raw + cleaned CSVs
python/     inventory.py
sql/        queries.sql
excel/      inventory_calculator.xlsx
powerbi/    inventory_dashboard.pbix
```

## Tech Stack
Python (pandas, numpy) · MySQL · Excel · Power BI (DAX)
