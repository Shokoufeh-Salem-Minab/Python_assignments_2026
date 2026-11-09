# Homework 7 - Sales Data Analysis
# Lasse Johannis

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ----- Part 5: Functions -----
def calculate_revenue(quantity, price):
    return quantity * price


def get_top_product(df):
    product_revenue = df.groupby("Product")["Total_Sales"].sum()
    return product_revenue.idxmax()


# ----- Part 2: Python and NumPy -----
with open("sales.csv", "r") as f:
    data = [line.strip().split(",") for line in f]

rows = data[1:]  # skip the header

products = [row[0] for row in rows]
print("Products:", products)

quantity_per_product = {}
for product, category, quantity, price, region in rows:
    if product in quantity_per_product:
        quantity_per_product[product] += int(quantity)
    else:
        quantity_per_product[product] = int(quantity)
print("Total quantity per product:", quantity_per_product)

quantities = np.array([int(row[2]) for row in rows])
print("Quantities:", quantities)
print("Total quantity sold:", np.sum(quantities))
print("Average quantity sold:", np.round(np.mean(quantities), 2))
print("Maximum quantity:", np.max(quantities))
print("Minimum quantity:", np.min(quantities))
print("Standard deviation:", np.round(np.std(quantities), 2))

indices = np.where(quantities > 5)[0]
print("Indices with quantity greater than 5:", indices)


# ----- Part 3: Pandas -----
df = pd.read_csv("sales.csv")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nDescriptive statistics:")
print(df.describe())

df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])

total_revenue = df["Total_Sales"].sum()
print("\nTotal revenue:", total_revenue)

top_product = get_top_product(df)
print("Product with the highest revenue:", top_product)

category_revenue = df.groupby("Category")["Total_Sales"].sum()
print("\nRevenue per category:")
print(category_revenue)

region_sales = df.groupby("Region")["Total_Sales"].sum()
best_region = region_sales.idxmax()
print("\nRegion with the highest sales:", best_region)

df = df.sort_values("Total_Sales", ascending=False)
print("\nSorted by Total_Sales:")
print(df)

df.to_csv("updated_sales.csv", index=False)
print("\nSaved to updated_sales.csv")


# ----- Part 4: Data Visualization -----
product_revenue = df.groupby("Product")["Total_Sales"].sum()

# 1. Bar chart
plt.bar(product_revenue.index, product_revenue.values, color="green")
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.xticks(rotation=15)
plt.ylabel("Revenue (EUR)")
plt.tight_layout()
plt.savefig("bar_chart.png")
plt.show()

# 2. Pie chart
plt.pie(category_revenue.values, labels=category_revenue.index, autopct="%1.1f%%")
plt.title("Revenue Share by Category")
plt.savefig("pie_chart.png")
plt.show()

# 3. Histogram
plt.hist(df["Total_Sales"], bins=6, color="orange", edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Revenue per Sale (EUR)")
plt.ylabel("Number of Sales")
plt.savefig("histogram.png")
plt.show()
