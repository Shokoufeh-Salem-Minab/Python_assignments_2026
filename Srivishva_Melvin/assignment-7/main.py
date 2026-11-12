# Homework 7
# Srivishva Melvin - sm25017
# Program created on: 10/11/2026

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg") # save the charts as files, no window needed
import matplotlib.pyplot as plt

def calculate_revenue(quantity, price):
    return quantity * price

def get_top_product(df):
    revenue_per_product = df.groupby("Product")["Total_Sales"].sum()
    return revenue_per_product.idxmax()

df = pd.read_csv("sales.csv") # reads the data

product_names = df["Product"].tolist()
quantity_per_product = {}
for name, quantity in zip(df["Product"], df["Quantity"]):
    quantity_per_product[name] = quantity_per_product.get(name, 0) + quantity

quantities = np.array(df["Quantity"])
print("Product names:", product_names)
print("Total quantity per product:", quantity_per_product)
print("Total quantity sold:", quantities.sum())
print("Average quantity sold:", round(quantities.mean(), 2))
print("Maximum quantity:", quantities.max(), "and minimum quantity:", quantities.min())
print("Standard deviation:", round(quantities.std(), 2))
print("Indices where quantity > 5:", np.where(quantities > 5)[0])

print("\nFirst 5 rows:")
print(df.head())
print("\nInfo:")
df.info()
print("\nDescriptive statistics:")
print(df.describe())
df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])

print("\nTotal revenue:", df["Total_Sales"].sum())
print("Product with the highest sales revenue:", get_top_product(df))
print("\nRevenue per category:")
print(df.groupby("Category")["Total_Sales"].sum())
print("\nRegion with the highest sales:", df.groupby("Region")["Total_Sales"].sum().idxmax())

df = df.sort_values("Total_Sales", ascending=False)
df.to_csv("updated_sales.csv", index=False)
print("\nSaved updated_sales.csv")

revenue_per_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(revenue_per_product.index, revenue_per_product.values, color="steelblue")
plt.title("Total Revenue per Product")
plt.xlabel("Product")
plt.ylabel("Total revenue")
plt.tight_layout()
plt.savefig("barChart.png")
plt.close()

revenue_per_category = df.groupby("Category")["Total_Sales"].sum()
plt.figure(figsize=(7, 7))
plt.pie(revenue_per_category.values, labels=revenue_per_category.index,
        autopct="%1.1f%%", startangle=90)
plt.title("Share of Total Revenue per Category")
plt.tight_layout()
plt.savefig("pieChart.png")
plt.close()

plt.figure(figsize=(8, 5))
plt.hist(df["Total_Sales"], bins=6, color="seagreen", edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Revenue per sale record")
plt.ylabel("Number of records")
plt.tight_layout()
plt.savefig("histogram.png")
plt.close()

print("Saved the 3 charts")
