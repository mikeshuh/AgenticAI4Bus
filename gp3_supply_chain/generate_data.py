"""
Generate synthetic supply chain data for inventory replenishment agent.

Creates three CSV files:
1. sales.csv - 90 days of demand data for 3 SKUs
2. inventory.csv - opening stock levels
3. params.csv - cost and policy parameters per SKU
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Generate dates (90 days)
start_date = datetime(2024, 8, 1)
dates = [start_date + timedelta(days=i) for i in range(90)]

# SKU-A: Stable demand (~50 units/day, low variance)
demand_a = np.random.normal(50, 5, 90).clip(30, 70).round().astype(int)

# SKU-B: Trending demand (starts ~20, grows to ~35, medium variance)
trend_b = np.linspace(20, 35, 90)
demand_b = (trend_b + np.random.normal(0, 4, 90)).clip(10, 50).round().astype(int)

# SKU-C: Volatile demand (~10 units/day, high variance with spikes)
base_c = np.random.normal(10, 6, 90)
# Add random spikes (20% chance of 2x demand)
spikes = np.random.random(90) < 0.2
base_c[spikes] *= 2
demand_c = base_c.clip(2, 30).round().astype(int)

# Create sales.csv
sales_data = []
for day_idx, date in enumerate(dates):
    sales_data.append({'date': date.strftime('%Y-%m-%d'), 'sku': 'SKU-A', 'qty_sold': demand_a[day_idx]})
    sales_data.append({'date': date.strftime('%Y-%m-%d'), 'sku': 'SKU-B', 'qty_sold': demand_b[day_idx]})
    sales_data.append({'date': date.strftime('%Y-%m-%d'), 'sku': 'SKU-C', 'qty_sold': demand_c[day_idx]})

sales_df = pd.DataFrame(sales_data)
sales_df.to_csv('sales.csv', index=False)
print(f"✓ Created sales.csv: {len(sales_df)} rows")

# Create inventory.csv
inventory_df = pd.DataFrame([
    {'sku': 'SKU-A', 'opening_stock': 200},
    {'sku': 'SKU-B', 'opening_stock': 100},
    {'sku': 'SKU-C', 'opening_stock': 50}
])
inventory_df.to_csv('inventory.csv', index=False)
print(f"✓ Created inventory.csv: {len(inventory_df)} rows")

# Create params.csv
params_df = pd.DataFrame([
    {
        'sku': 'SKU-A',
        'unit_cost': 15.00,
        'holding_cost_per_day': 0.08,  # ~0.5% of unit cost per day
        'stockout_cost': 45.00,  # 3x unit cost
        'lead_time_days': 3,
        'min_order_qty': 100,
        'service_level': 0.98
    },
    {
        'sku': 'SKU-B',
        'unit_cost': 30.00,
        'holding_cost_per_day': 0.15,
        'stockout_cost': 90.00,
        'lead_time_days': 7,
        'min_order_qty': 50,
        'service_level': 0.95
    },
    {
        'sku': 'SKU-C',
        'unit_cost': 25.00,
        'holding_cost_per_day': 0.12,
        'stockout_cost': 75.00,
        'lead_time_days': 5,
        'min_order_qty': 30,
        'service_level': 0.90
    }
])
params_df.to_csv('params.csv', index=False)
print(f"✓ Created params.csv: {len(params_df)} rows")

# Display summary statistics
print("\nDemand Summary:")
print(f"SKU-A (Stable): Mean={demand_a.mean():.1f}, Std={demand_a.std():.1f}, Range=[{demand_a.min()}-{demand_a.max()}]")
print(f"SKU-B (Trending): Mean={demand_b.mean():.1f}, Std={demand_b.std():.1f}, Range=[{demand_b.min()}-{demand_b.max()}]")
print(f"SKU-C (Volatile): Mean={demand_c.mean():.1f}, Std={demand_c.std():.1f}, Range=[{demand_c.min()}-{demand_c.max()}]")
