import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

products = []
quantities = []
prices = []
product_quantities = {}

with open('sales.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row['Product']
        qty = int(row['Quantity'])
        price = float(row['Price'])
        
        products.append(product)
        quantities.append(qty)
        prices.append(price)
        
        if product in product_quantities:
            product_quantities[product] += qty
        else:
            product_quantities[product] = qty

print(products)
print(product_quantities)

quantities_array = np.array(quantities)

print(np.sum(quantities_array))
print(np.mean(quantities_array))
print(np.max(quantities_array))
print(np.min(quantities_array))
print(np.std(quantities_array))

indices_greater_than_5 = np.where(quantities_array > 5)[0]
print(indices_greater_than_5)

df = pd.read_csv('sales.csv')

print(df.head())
df.info()
print(df.describe())

df['Total_Sales'] = df['Quantity'] * df['Price']

total_revenue = df['Total_Sales'].sum()
print(total_revenue)

revenue_by_product = df.groupby('Product')['Total_Sales'].sum()
top_product = revenue_by_product.idxmax()
print(top_product)

revenue_by_category = df.groupby('Category')['Total_Sales'].sum()
print(revenue_by_category)

revenue_by_region = df.groupby('Region')['Total_Sales'].sum()
top_region = revenue_by_region.idxmax()
print(top_region)

df_sorted = df.sort_values(by='Total_Sales', ascending=False)
df_sorted.to_csv('updated_sales.csv', index=False)

plt.figure(figsize=(10, 5))
revenue_by_product.plot(kind='bar', color='skyblue')
plt.title('Total Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('bar_chart.png')

plt.figure(figsize=(8, 8))
revenue_by_category.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'salmon'])
plt.title('Revenue Share by Category')
plt.ylabel('')
plt.savefig('pie_chart.png')

plt.figure(figsize=(10, 5))
plt.hist(df['Total_Sales'], bins=10, color='purple', edgecolor='black')
plt.title('Distribution of Sales Revenue')
plt.xlabel('Sales Revenue per Transaction ($)')
plt.ylabel('Frequency')
plt.savefig('histogram.png')

def calculate_revenue(quantity, price):
    return quantity * price

def get_top_product(dataframe):
    rev_by_prod = dataframe.groupby('Product')['Total_Sales'].sum()
    return rev_by_prod.idxmax()
