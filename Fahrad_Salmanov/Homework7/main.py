import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_revenue(quantity, price):
    """fucntion to  calculate revenue"""
    return quantity * price


def get_top_product(df):
    """Return the name and revenue of the product with the highest revenue."""
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum()
    return revenue_by_product.idxmax(), revenue_by_product.max()

# ---------- Part 3: Pandas ----------
df = pd.read_csv("sales.csv")

print(df.head())       # 1. first 5 rows
df.info()              # 2. dataset information
print(df.describe())   # 3. descriptive statistics

# 4. New column with calculated revenue
df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])
print(df.head())

# 5. Total revenue
total_revenue = df["Total_Sales"].sum()
print("Total revenue:", total_revenue)

# 6. Product with the highest revenue
top_product, top_revenue = get_top_product(df)
print("Top product:", top_product, top_revenue)

# 7. Revenue per category
revenue_by_category = df.groupby("Category")["Total_Sales"].sum()
print("Revenue by category:")
print(revenue_by_category)

# 8. Region with the highest sales
revenue_by_region = df.groupby("Region")["Total_Sales"].sum()
print("Revenue by region:")
print(revenue_by_region)
print("Best region:", revenue_by_region.idxmax())

# 9. Sort by Total_Sales, highest first
df_sorted = df.sort_values(by="Total_Sales", ascending=False)
print(df_sorted)

# 10. Save to a new CSV
df_sorted.to_csv("updated_sales.csv", index=False)

# Revenue per product (to be used for putting biggest revenue product in the bar chart)
revenue_by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)

#bar chart for revenue by product
plt.figure(figsize=(8, 5))
plt.bar(revenue_by_product.index, revenue_by_product.values ,color='skyblue')
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("bar_chart.png", dpi=150)
plt.show()

# 2. Pie chart
plt.figure(figsize=(6, 6))
plt.pie(revenue_by_category.values, labels=revenue_by_category.index,
        autopct="%1.1f%%", startangle=90)
plt.title("Share of Total Revenue by Category")
plt.tight_layout()
plt.savefig("pie_chart.png", dpi=150)
plt.show()

# 3. Histogram
plt.figure(figsize=(8, 5))
plt.hist(df["Total_Sales"], bins=8, color="seagreen", edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Revenue per sale")
plt.ylabel("Number of sales")
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.show()

#Part 2: Python and NumPy 

# 1. Product names into a list (and quantities, which i need later)
products = []
quantities = []

with open("sales.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append(row["Product"])
        quantities.append(int(row["Quantity"]))

print("Products:", products)

# 2. Dictionary with total quantity sold per product
quantity_per_product = {}
for product, qty in zip(products, quantities):
    quantity_per_product[product] = quantity_per_product.get(product, 0) + qty

print("Total quantity per product:", quantity_per_product)

# 3. NumPy array with all quantities
qty_array = np.array(quantities)
print("Quantities array:", qty_array)

# 4. Statistics
print("Total quantity sold:", qty_array.sum())
print("Average quantity sold:", qty_array.mean())
print("Maximum quantity:", qty_array.max())
print("Minimum quantity:", qty_array.min())
print("Standard deviation:", qty_array.std())

# 5. Indices where quantity is greater than 5
indices = np.where(qty_array > 5)[0]
print("Indices where quantity > 5:", indices)