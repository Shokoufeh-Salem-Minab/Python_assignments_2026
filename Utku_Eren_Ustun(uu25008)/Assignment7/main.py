import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

products = []
quantities = []
product_totals = {}

with open("sales.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row["Product"]
        quantity = int(row["Quantity"])
        products.append(product)
        quantities.append(quantity)
        product_totals[product] = product_totals.get(product, 0) + quantity

print("Product names list:", products)
print("Total quantity sold per product:", product_totals)

qty_array = np.array(quantities)
total_qty = np.sum(qty_array)
avg_qty = np.mean(qty_array)
max_qty = np.max(qty_array)
min_qty = np.min(qty_array)
std_qty = np.std(qty_array)
indices_gt_5 = np.where(qty_array > 5)[0]

print("Total quantity sold:", total_qty)
print("Average quantity sold:", avg_qty)
print("Maximum quantity:", max_qty)
print("Minimum quantity:", min_qty)
print("Standard deviation:", std_qty)
print("Indices where quantity > 5:", indices_gt_5)

df = pd.read_csv("sales.csv")
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset info:")
df.info()
print("\nDescriptive statistics:")
print(df.describe())
df["Total_Sales"] = df["Quantity"] * df["Price"]

total_revenue = df["Total_Sales"].sum()
product_revenue = df.groupby("Product")["Total_Sales"].sum()
highest_revenue_product = product_revenue.idxmax()
category_revenue = df.groupby("Category")["Total_Sales"].sum()
region_revenue = df.groupby("Region")["Total_Sales"].sum()
highest_sales_region = region_revenue.idxmax()

print("\nTotal revenue:", total_revenue)
print("Product with highest sales revenue:", highest_revenue_product)
print("\nTotal revenue by category:")
print(category_revenue)
print("\nRegion with highest sales:", highest_sales_region)

df_sorted = df.sort_values(by="Total_Sales", ascending=False)
df_sorted.to_csv("updated_sales.csv", index=False)

plt.figure(figsize=(8, 5))
product_revenue.plot(kind="bar", color="steelblue", edgecolor="black")
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Total Revenue ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("bar_chart.png")
plt.close()

# Pie Chart
plt.figure(figsize=(7, 7))
plt.pie(
    category_revenue,
    labels=category_revenue.index,
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Percentage of Total Revenue by Category")
plt.tight_layout()
plt.savefig("pie_chart.png")
plt.close()

# Histogram
plt.figure(figsize=(8, 5))
plt.hist(df["Total_Sales"], bins=6, color="teal", edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Sales Revenue ($)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("histogram.png")
plt.close()

def calculate_revenue(quantity, price):
    return quantity * price

def get_top_product(dataframe):
    df_copy = dataframe.copy()
    if "Total_Sales" not in df_copy.columns:
        df_copy["Total_Sales"] = calculate_revenue(df_copy["Quantity"], df_copy["Price"])
    return df_copy.groupby("Product")["Total_Sales"].sum().idxmax()