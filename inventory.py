import pandas as pd
import numpy as np

df = pd.read_csv("e:/project/DataCoSupplyChainDataset.csv", encoding = "latin1")

# print(df.shape)
# print(df.isnull().sum())
# print(df.columns.to_list())



df.drop(columns = ['Product Description', 'Order Zipcode', 'Customer Email', 'Customer Password',
             'Customer Fname', 'Customer Lname', 'Customer Street', 'Latitude', 'Longitude',
             'Product Image', 'Customer Zipcode'], inplace = True)

# print(df.isnull().sum())
# print(df.shape)


df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
df['shipping date (DateOrders)'] = pd.to_datetime(df['shipping date (DateOrders)'])
# print(df['order date (DateOrders)'].head())
# print(df['shipping date (DateOrders)'].head())
      
      
demand_df = df[df['Order Status'].isin(['COMPLETE', 'CLOSED'])]
# print(demand_df)

df.to_csv("e:/project/cleaned_inventory.csv", index = False)
demand_df.to_csv("e:/project/demand.csv", index = False)
# print("Files saved successfully.")

product_revenue = demand_df.groupby('Product Card Id')['Sales'].sum().sort_values(ascending = False)
# print(product_revenue.head())

cumulative_revenue = product_revenue.cumsum()
total_revenue = product_revenue.sum()
cumulative_percent = (cumulative_revenue/total_revenue) * 100
# print(cumulative_percent.head(10))

abc_class = []

for percent in cumulative_percent:
    if percent <= 70:
        abc_class.append('A')
    else:
        if percent <= 90:
            abc_class.append('B')
        else:
            abc_class.append('C')

abc_table = pd.DataFrame({
    'Product Card Id' : product_revenue.index,
    'Total Revenue' : product_revenue.values,
    'Cumulative Revenue' : cumulative_revenue.values,
    'Cumulative Percent' : cumulative_percent.values,
    'ABC Class' : abc_class
})

# print(abc_table.head(10))
# print(abc_table.groupby('ABC Class').value_counts())
abc_table.to_csv("e:/project/abc_class.csv", index = False)
# print("ABC saved")

demand_df = demand_df.merge(abc_table[['Product Card Id', 'ABC Class']], on = 'Product Card Id', how='left')
# print(demand_df.head())

demand_df.to_csv("e:/project/demand_with_abc.csv", index = False)
# print("Demand with ABC saved")

product_quantity = demand_df.groupby('Product Card Id')['Order Item Quantity'].sum()
# print(product_quantity.head(10))

annual_demand = product_quantity / 3
# print(annual_demand.head(10))


unit_price = demand_df.groupby('Product Card Id')['Order Item Product Price'].mean()
# print(unit_price.head(10))


ordering_cost = 50


cost_table = pd.DataFrame({
    'Product Card Id' : unit_price.index,
    'Unit_price' : unit_price.values
})

cost_table = cost_table.merge(abc_table[['Product Card Id', 'ABC Class']], on = 'Product Card Id', how='left')
# print(cost_table.head(10))

holding_cost_list = []

for cls in cost_table['ABC Class']:
    if cls == 'A':
        holding_cost_list.append(0.25)
    elif cls == 'B':
        holding_cost_list.append(0.15)
    else:
        holding_cost_list.append(0.10)
        
cost_table['Holding_Cost_Percent'] = holding_cost_list
cost_table['Holding_Cost'] = cost_table['Unit_price'] * cost_table['Holding_Cost_Percent']
# print(cost_table.head(10))

cost_table['Annual_Demand'] = annual_demand.values

# print(len(cost_table), len(annual_demand))

cost_table['EOQ'] =np.sqrt((2 * cost_table['Annual_Demand'] * ordering_cost) / cost_table['Holding_Cost'])
# print(cost_table.head(10))

cost_table.to_csv("e:/project/eoq_analysis.csv", index = False)
# print("EOQ analysis saved")

daily_demand = demand_df.groupby(['Product Card Id', demand_df['order date (DateOrders)'].dt.date])['Order Item Quantity'].sum()
# print(daily_demand.head(10))

demand_stats = daily_demand.groupby('Product Card Id').agg(['mean', 'std'])
# print(demand_stats.head(10))

lead_time = demand_df.groupby('Product Card Id')['Days for shipping (real)'].mean()
# print(lead_time.head(10))

final_table = pd.DataFrame({
    'Product Card Id' : demand_stats.index,
    'Avg_Daily_Demand' : demand_stats[('mean')].values,
    'Std_Daily_Demand' : demand_stats[('std')].values,
})

final_table = final_table.merge(cost_table[['Product Card Id', 'ABC Class', 'Annual_Demand', 'EOQ']], on = 'Product Card Id', how='left')
final_table['Lead_time'] = lead_time.values
# print(final_table.head(10))

z_score_list = []

for cls in final_table['ABC Class']:
    if cls == 'A':
        z_score_list.append(2.05)
    elif cls == 'B':
        z_score_list.append(1.65)
    else:
        z_score_list.append(1.28)
        
final_table['z_score'] = z_score_list
# print(final_table.head(10))

final_table['Safety_stock'] = final_table['z_score'] * final_table['Std_Daily_Demand'] * np.sqrt(final_table['Lead_time'])
# print(final_table.head(10))

final_table['ROP'] = (final_table['Avg_Daily_Demand'] * final_table['Lead_time']) + final_table['Safety_stock']
# print(final_table.head(10))

final_table.to_csv("e:/project/final_inventory_analysis.csv", index = False)
# print("Success")

print(final_table.columns.tolist())
print(final_table.columns[final_table.columns.duplicated()])