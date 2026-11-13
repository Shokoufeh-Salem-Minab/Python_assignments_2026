# Andre Filho - Homework 7 - Sales Data Analysis

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

folder = os.path.dirname(os.path.abspath(__file__))
sales_path = os.path.join(folder, "sales.csv")


# part 5: revenue of a sale
def calculate_revenue(quantity, price):
    return quantity * price


# part 5: product with the highest revenue
def get_top_product(df):
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum()
    return revenue_by_product.idxmax()


def part_2_numpy():
    print("=== Part 2: Python and NumPy ===")

    # read the product names and quantities from the csv file
    products = []
    quantities = []
    with open(sales_path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row["Product"])
            quantities.append(int(row["Quantity"]))

    print("Products:", products)

    # total quantity sold for each product
    totals = {}
    for product, quantity in zip(products, quantities):
        if product in totals:
            totals[product] += quantity
        else:
            totals[product] = quantity
    print("Total quantity per product:", totals)

    quantity_array = np.array(quantities)
    print("Quantities array:", quantity_array)
    print("Total quantity sold:", quantity_array.sum())
    print("Average quantity sold:", round(quantity_array.mean(), 2))
    print("Maximum quantity:", quantity_array.max())
    print("Minimum quantity:", quantity_array.min())
    print("Standard deviation:", round(quantity_array.std(), 2))

    # indices of the sales where quantity is greater than 5
    indices = np.where(quantity_array > 5)[0]
    print("Indices with quantity > 5:", indices)


def part_3_pandas():
    print("\n=== Part 3: Pandas ===")
    df = pd.read_csv(sales_path)

    print("First 5 rows:")
    print(df.head())

    print("\nDataset info:")
    df.info()

    print("\nDescriptive statistics:")
    print(df.describe())

    df["Total_Sales"] = df["Quantity"] * df["Price"]

    total_revenue = df["Total_Sales"].sum()
    print("\nTotal revenue:", round(total_revenue, 2))

    print("Product with the highest sales revenue:", get_top_product(df))

    print("\nTotal revenue per category:")
    print(df.groupby("Category")["Total_Sales"].sum().round(2))

    region_revenue = df.groupby("Region")["Total_Sales"].sum()
    print("\nRegion with the highest sales:", region_revenue.idxmax())

    df = df.sort_values("Total_Sales", ascending=False)
    print("\nSorted by Total_Sales (descending):")
    print(df.round(2))

    df.to_csv(os.path.join(folder, "updated_sales.csv"), index=False)
    return df


def part_4_charts(df):
    print("\n=== Part 4: Charts ===")

    # 1. bar chart: revenue per product
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum()
    plt.figure(figsize=(8, 5))
    plt.bar(revenue_by_product.index, revenue_by_product.values, color="steelblue")
    plt.title("Total Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "bar_chart.png"))
    plt.close()

    # 2. pie chart: share of revenue per category
    revenue_by_category = df.groupby("Category")["Total_Sales"].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(revenue_by_category.values, labels=revenue_by_category.index, autopct="%1.1f%%")
    plt.title("Share of Total Revenue by Category")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "pie_chart.png"))
    plt.close()

    # 3. histogram: distribution of the sales revenue
    plt.figure(figsize=(8, 5))
    plt.hist(df["Total_Sales"], bins=6, color="seagreen", edgecolor="black")
    plt.title("Distribution of Sales Revenue")
    plt.xlabel("Revenue of one sale")
    plt.ylabel("Number of sales")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, "histogram.png"))
    plt.close()

    print("Saved bar_chart.png, pie_chart.png and histogram.png")


if __name__ == "__main__":
    part_2_numpy()
    sales_df = part_3_pandas()
    part_4_charts(sales_df)

    print("\n=== Part 5: Functions ===")
    print("calculate_revenue(3, 899.99) =", round(calculate_revenue(3, 899.99), 2))
    print("Top product:", get_top_product(sales_df))
