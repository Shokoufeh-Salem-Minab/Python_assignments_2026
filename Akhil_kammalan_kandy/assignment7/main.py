"""Sales data analysis for Assignment 7."""


from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales.csv"


def calculate_revenue(quantity, price):
    """Return the revenue earned from a quantity sold at a unit price."""
    return quantity * price


def get_top_product(dataframe):
    """Return the product name and its total revenue, highest first."""
    revenue_by_product = dataframe.groupby("Product")["Total_Sales"].sum()
    product = revenue_by_product.idxmax()
    return product, revenue_by_product[product]


def create_charts(dataframe):
    """Create and save the three charts requested in the assignment."""
    product_revenue = dataframe.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    category_revenue = dataframe.groupby("Category")["Total_Sales"].sum()

    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(9, 5))
    product_revenue.plot(kind="bar", color="#4C78A8", ax=ax)
    ax.set_title("Total Revenue by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Revenue (EUR)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "product_revenue_bar_chart.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 7))
    category_revenue.plot(
        kind="pie", autopct="%1.1f%%", startangle=90,
        colors=["#4C78A8", "#F58518"], ax=ax,
    )
    ax.set_title("Percentage of Total Revenue by Category")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(BASE_DIR / "category_revenue_pie_chart.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(dataframe["Total_Sales"], bins=8, color="#54A24B", edgecolor="white")
    ax.set_title("Distribution of Sales Revenue per Record")
    ax.set_xlabel("Sales Revenue (EUR)")
    ax.set_ylabel("Number of Sales Records")
    fig.tight_layout()
    fig.savefig(BASE_DIR / "sales_revenue_histogram.png", dpi=150)
    plt.close(fig)


def main():
    # Python and NumPy analysis.
    dataframe = pd.read_csv(DATA_FILE)
    product_names = dataframe["Product"].tolist()
    quantities_by_product = dataframe.groupby("Product")["Quantity"].sum().to_dict()
    quantities = dataframe["Quantity"].to_numpy()

    print("Product names:", product_names)
    print("Total quantity sold by product:", quantities_by_product)
    print("Total quantity sold:", quantities.sum())
    print(f"Average quantity sold: {quantities.mean():.2f}")
    print("Maximum quantity:", quantities.max())
    print("Minimum quantity:", quantities.min())
    print(f"Standard deviation: {quantities.std():.2f}")
    print("Indices where quantity is greater than 5:", np.where(quantities > 5)[0].tolist())

    # Pandas analysis.
    print("\nFirst 5 rows:\n", dataframe.head())
    print("\nDataset information:")
    dataframe.info()
    print("\nDescriptive statistics:\n", dataframe.describe(include="all"))

    dataframe["Total_Sales"] = calculate_revenue(dataframe["Quantity"], dataframe["Price"])
    total_revenue = dataframe["Total_Sales"].sum()
    top_product, top_product_revenue = get_top_product(dataframe)
    revenue_by_category = dataframe.groupby("Category")["Total_Sales"].sum()
    revenue_by_region = dataframe.groupby("Region")["Total_Sales"].sum()
    best_region = revenue_by_region.idxmax()

    updated_dataframe = dataframe.sort_values("Total_Sales", ascending=False)
    updated_dataframe.to_csv(BASE_DIR / "updated_sales.csv", index=False)
    create_charts(dataframe)

    print(f"\nTotal revenue: EUR {total_revenue:,.2f}")
    print(f"Highest-revenue product: {top_product} (EUR {top_product_revenue:,.2f})")
    print("Revenue by category:\n", revenue_by_category)
    print(f"Region with the highest sales: {best_region} (EUR {revenue_by_region[best_region]:,.2f})")
    print("\nUpdated data saved to updated_sales.csv; charts saved as PNG files.")


if __name__ == "__main__":
    main()
