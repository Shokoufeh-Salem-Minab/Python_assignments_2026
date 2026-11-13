# Homework 7 - Mini Project: Sales Data Analysis

import csv
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# work relative to the folder of this file, so it runs from anywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALES_FILE = os.path.join(BASE_DIR, "sales.csv")
UPDATED_FILE = os.path.join(BASE_DIR, "updated_sales.csv")


# ---------------------------------------------------------------
# Part 5 - Functions
# ---------------------------------------------------------------

def calculate_revenue(quantity, price):
    """Returns the total revenue for a quantity and a price per item."""
    return quantity * price


def get_top_product(df):
    """Returns the product with the highest revenue and its revenue."""
    revenue_per_product = df.groupby("Product")["Total_Sales"].sum()
    top_product = revenue_per_product.idxmax()
    return top_product, revenue_per_product[top_product]


# ---------------------------------------------------------------
# Part 2 - Python and NumPy
# ---------------------------------------------------------------

def python_numpy_part():
    print("=" * 50)
    print("PART 2 - Python and NumPy")
    print("=" * 50)

    products = []
    quantities = []
    with open(SALES_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row["Product"])
            quantities.append(int(row["Quantity"]))

    print("Products:", products)

    # total quantity for each product
    quantity_per_product = {}
    for product, quantity in zip(products, quantities):
        quantity_per_product[product] = quantity_per_product.get(product, 0) + quantity
    print("Quantity per product:", quantity_per_product)

    q = np.array(quantities)
    print("Quantities array:", q)
    print("Total quantity sold:", q.sum())
    print(f"Average quantity sold: {q.mean():.2f}")
    print("Maximum quantity:", q.max())
    print("Minimum quantity:", q.min())
    print(f"Standard deviation: {q.std():.2f}")

    indices = np.where(q > 5)[0]
    print("Indices where quantity > 5:", indices)
    print("Products at these indices:", [products[i] for i in indices])
    print()


# ---------------------------------------------------------------
# Part 3 - Pandas
# ---------------------------------------------------------------

def pandas_part():
    print("=" * 50)
    print("PART 3 - Pandas")
    print("=" * 50)

    df = pd.read_csv(SALES_FILE)

    print("First 5 rows:")
    print(df.head())
    print()

    print("Dataset info:")
    df.info()
    print()

    print("Descriptive statistics:")
    print(df.describe())
    print()

    df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])

    total_revenue = df["Total_Sales"].sum()
    print(f"Total revenue: {total_revenue:.2f}")

    top_product, top_revenue = get_top_product(df)
    print(f"Product with highest revenue: {top_product} ({top_revenue:.2f})")

    revenue_per_category = df.groupby("Category")["Total_Sales"].sum()
    print("Revenue per category:")
    print(revenue_per_category)

    revenue_per_region = df.groupby("Region")["Total_Sales"].sum()
    best_region = revenue_per_region.idxmax()
    print(f"Region with highest sales: {best_region} ({revenue_per_region[best_region]:.2f})")
    print()

    df = df.sort_values("Total_Sales", ascending=False)
    print("Sorted by Total_Sales:")
    print(df)

    df.to_csv(UPDATED_FILE, index=False)
    print("Saved updated_sales.csv")
    print()

    return df


# ---------------------------------------------------------------
# Part 4 - Data Visualization
# ---------------------------------------------------------------

def visualization_part(df):
    print("=" * 50)
    print("PART 4 - Charts")
    print("=" * 50)

    # 1. Bar chart - revenue per product
    revenue_per_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    bars = plt.bar(revenue_per_product.index, revenue_per_product.values, color="steelblue")
    plt.bar_label(bars, fmt="%.0f")
    plt.title("Total Revenue per Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue (€)")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "bar_chart_revenue_per_product.png"))
    plt.close()

    # 2. Pie chart - revenue share per category
    revenue_per_category = df.groupby("Category")["Total_Sales"].sum()
    plt.figure(figsize=(7, 7))
    plt.pie(revenue_per_category.values, labels=revenue_per_category.index,
            autopct="%1.1f%%", startangle=90)
    plt.title("Share of Total Revenue by Category")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "pie_chart_revenue_by_category.png"))
    plt.close()

    # 3. Histogram - distribution of sales revenue
    plt.figure(figsize=(8, 5))
    plt.hist(df["Total_Sales"], bins=8, color="seagreen", edgecolor="black")
    plt.title("Distribution of Sales Revenue")
    plt.xlabel("Revenue per Sale (€)")
    plt.ylabel("Number of Sales")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "histogram_sales_revenue.png"))
    plt.close()

    print("Saved 3 charts as PNG files")


def main():
    python_numpy_part()
    df = pandas_part()
    visualization_part(df)


if __name__ == "__main__":
    main()
