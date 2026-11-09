import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ----- Global Settings -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALES_FILE = os.path.join(BASE_DIR, "sales.csv")
UPDATED_SALES_FILE = os.path.join(BASE_DIR, "updated_sales.csv")
BAR_CHART_FILE = os.path.join(BASE_DIR, "bar_chart.png")
PIE_CHART_FILE = os.path.join(BASE_DIR, "pie_chart.png")
HISTOGRAM_FILE = os.path.join(BASE_DIR, "histogram.png")

# ----- Chart Colors -----
MAIN_COLOR = "#2a78d6"
CATEGORY_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]


# ----- Part 5: Functions -----
def calculate_revenue(quantity, price):
    return quantity * price


def get_top_product(df):
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum()
    # idxmax() gives the label (product name) of the biggest value
    return revenue_by_product.idxmax()


# ----- Part 2: Python and NumPy -----
def analyze_with_python_and_numpy():
    with open(SALES_FILE, newline="") as file:
        rows = list(csv.DictReader(file))

    product_names = [row["Product"] for row in rows]

    # total quantity sold as {product: quantity}
    quantity_by_product = {}
    for row in rows:
        product = row["Product"]
        quantity_by_product[product] = quantity_by_product.get(product, 0) + int(row["Quantity"])

    quantities = np.array([int(row["Quantity"]) for row in rows])

    # positions in the array where the condition is True
    indices_above_5 = np.where(quantities > 5)[0]

    print("===== PART 2: PYTHON AND NUMPY =====")
    print("\nProduct names:", product_names)
    print("Quantity by product:", quantity_by_product)
    print("Quantities:", quantities)

    print("\n----- QUANTITY STATISTICS -----")
    print(f"Total: {quantities.sum()}")
    print(f"Average: {quantities.mean():.2f}")
    print(f"Maximum: {quantities.max()}")
    print(f"Minimum: {quantities.min()}")
    # np.std() is the population formula, describe() in Part 3 is the sample formula,
    # so the two standard deviations are slightly different
    print(f"Standard deviation: {quantities.std():.2f}")

    print("\nIndices where quantity > 5:", indices_above_5)


# ----- Part 3: Pandas -----
def show_dataset_overview(df):
    print("\n===== PART 3: PANDAS =====")

    print("\n----- FIRST 5 ROWS -----")
    print(df.head())

    print("\n----- DATASET INFORMATION -----")
    df.info()  # info() prints by itself and returns None

    print("\n----- DESCRIPTIVE STATISTICS -----")
    print(df.describe())


def show_revenue_analysis(df):
    total_revenue = df["Total_Sales"].sum()
    revenue_by_category = df.groupby("Category")["Total_Sales"].sum()
    revenue_by_region = df.groupby("Region")["Total_Sales"].sum()

    print("\n----- REVENUE ANALYSIS -----")
    print(f"Total revenue: {total_revenue:.2f}")
    print(f"Product with the highest revenue: {get_top_product(df)}")
    print(f"Region with the highest sales: {revenue_by_region.idxmax()}")

    print("\nRevenue by category:")
    print(revenue_by_category)

    print("\nRevenue by region:")
    print(revenue_by_region)


def analyze_with_pandas():
    df = pd.read_csv(SALES_FILE)
    show_dataset_overview(df)

    # the function also works on whole columns: each row is multiplied by its own price
    df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])
    show_revenue_analysis(df)

    df = df.sort_values("Total_Sales", ascending=False)
    df.to_csv(UPDATED_SALES_FILE, index=False)

    print("\n----- SORTED BY TOTAL SALES -----")
    print(df.to_string(index=False))
    print(f"\nUpdated data saved to {UPDATED_SALES_FILE}")

    return df


# ----- Part 4: Charts -----
def save_chart(path):
    plt.tight_layout()  # keeps the labels inside the image
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Chart saved to {path}")


def create_bar_chart(df):
    revenue = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(revenue.index, revenue.values, color=MAIN_COLOR, width=0.6)
    plt.bar_label(bars, fmt="%.0f", padding=3)  # writes the value above each bar
    plt.title("Total Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Revenue ($)")
    plt.grid(axis="y", alpha=0.3)
    save_chart(BAR_CHART_FILE)


def create_pie_chart(df):
    revenue = df.groupby("Category")["Total_Sales"].sum()

    plt.figure(figsize=(7, 7))
    plt.pie(
        revenue.values,
        labels=revenue.index,
        colors=CATEGORY_COLORS,
        autopct="%1.1f%%",  # writes the percentage on each slice
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    plt.title("Share of Total Revenue by Category")
    save_chart(PIE_CHART_FILE)


def create_histogram(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df["Total_Sales"], bins=8, color=MAIN_COLOR, edgecolor="white", linewidth=2)
    plt.title("Distribution of Sales Revenue")
    plt.xlabel("Revenue per Sales Record ($)")
    plt.ylabel("Number of Sales Records")
    plt.grid(axis="y", alpha=0.3)
    save_chart(HISTOGRAM_FILE)


def create_charts(df):
    print("\n===== PART 4: CHARTS =====")
    create_bar_chart(df)
    create_pie_chart(df)
    create_histogram(df)


def main():
    analyze_with_python_and_numpy()
    df = analyze_with_pandas()
    create_charts(df)


if __name__ == "__main__":
    main()
