import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_revenue(quantity, price):
    return quantity * price

def get_top_product(df):
    revenue = df.groupby("Product")["Total_Sales"].sum()
    return revenue.idxmax(), revenue.max()

with open("sales.csv", newline="") as file:
    rows = list(csv.DictReader(file))

products = [row["Product"] for row in rows]

product_quantities = {}
for row in rows:
    product_quantities[row["Product"]] = product_quantities.get(row["Product"], 0) + int(row["Quantity"])

quantities = np.array([int(row["Quantity"]) for row in rows])

print(f"Products: {products}")
print(f"Quantity by product: {product_quantities}")
print(f"Quantities: {quantities}")

print("\nQuantity statistics:")
print(f"Total: {quantities.sum()}")
print(f"Average: {quantities.mean():.2f}")
print(f"Max: {quantities.max()}")
print(f"Min: {quantities.min()}")
print(f"Std: {quantities.std():.2f}")

high_indices = np.where(quantities > 5)[0]
print(f"\nIndices with quantity > 5: {high_indices}")
print(f"Products with quantity > 5: {np.array(products)[high_indices]}")

df = pd.read_csv("sales.csv")

print("\nFirst 5 rows:")
print(df.head())

print("\nInfo:")
df.info()

print("\nDescriptive statistics:")
print(df.describe().round(2))

df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])

top_product, top_revenue = get_top_product(df)
category_revenue = df.groupby("Category")["Total_Sales"].sum().sort_values(ascending=False)
region_revenue = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
product_revenue = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)

print(f"\nTotal revenue: {df['Total_Sales'].sum()}")
print(f"Top product: {top_product} ({top_revenue})")

print("\nRevenue by category:")
print(category_revenue)

print(f"\nBest region: {region_revenue.idxmax()} ({region_revenue.max()})")
print(region_revenue)

ranked = df.sort_values("Total_Sales", ascending=False)
print("\nSorted by Total_Sales:")
print(ranked)

ranked.to_csv("updated_sales.csv", index=False)
print("\nData saved to updated_sales.csv")

plt.figure(figsize=(8, 5))
plt.bar(product_revenue.index, product_revenue.values, color="steelblue")
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("revenue_by_product.png")

plt.figure(figsize=(6, 6))
plt.pie(category_revenue.values, labels=category_revenue.index, autopct="%1.1f%%", startangle=90)
plt.title("Revenue Share by Category")
plt.axis("equal")
plt.tight_layout()
plt.savefig("revenue_by_category.png")

plt.figure(figsize=(8, 5))
plt.hist(df["Total_Sales"], bins=6, color="seagreen", edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Revenue per sale")
plt.ylabel("Number of sales")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("revenue_histogram.png")

print("Charts saved: revenue_by_product.png, revenue_by_category.png, revenue_histogram.png")

plt.show()
