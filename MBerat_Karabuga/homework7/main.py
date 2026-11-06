import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Allows chart generation without a GUI.
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent


def calculate_revenue(quantity, price):
    #Return quantity multiplied by price
    return quantity * price


def get_top_product(dataframe):
    #Return the name and combined revenue of the best-selling product
    product_revenue = dataframe.groupby("Product")["Total_Sales"].sum()
    top_product = product_revenue.idxmax()
    return top_product, float(product_revenue.loc[top_product])


def main():
    # PART 2: Python and NumPy
    with (BASE_DIR / "sales.csv").open(newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    product_names = [row["Product"] for row in records]
    quantity_by_product = {}
    for row in records:
        product = row["Product"]
        quantity_by_product[product] = (
            quantity_by_product.get(product, 0) + int(row["Quantity"])
        )

    quantities = np.array([int(row["Quantity"]) for row in records])
    indices_over_five = np.where(quantities > 5)[0]

    print("PART 2: PYTHON AND NUMPY")
    print("Product names (Python list):", product_names)
    print("Total quantity per product (dictionary):", quantity_by_product)
    print("Quantity NumPy array:", quantities)
    print("Total quantity sold:", np.sum(quantities))
    print(f"Average quantity sold: {np.mean(quantities):.2f}")
    print("Maximum quantity:", np.max(quantities))
    print("Minimum quantity:", np.min(quantities))
    print(f"Standard deviation (population): {np.std(quantities):.2f}")
    print("Zero-based indices where quantity > 5:", indices_over_five.tolist())

    # PART 3: Pandas
    df = pd.read_csv(BASE_DIR / "sales.csv")
    print("\nPART 3: PANDAS")
    print("\nFirst five rows:\n", df.head())
    print("\nDataset information:")
    df.info()
    print("\nDescriptive statistics:\n", df.describe())

    df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])
    total_revenue = float(df["Total_Sales"].sum())
    top_product, top_product_revenue = get_top_product(df)
    category_revenue = df.groupby("Category")["Total_Sales"].sum().sort_values(ascending=False)
    region_revenue = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    product_revenue = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    top_region = region_revenue.idxmax()
    top_category = category_revenue.idxmax()

    print(f"\nTotal revenue: ${total_revenue:,.2f}")
    print(f"Highest-revenue product: {top_product} (${top_product_revenue:,.2f})")
    print("\nRevenue by category:\n", category_revenue.to_string())
    print("\nRevenue by region:\n", region_revenue.to_string())
    print("\nSorted sales records (highest revenue first):\n",
          df.sort_values("Total_Sales", ascending=False).to_string(index=False))

    sorted_df = df.sort_values("Total_Sales", ascending=False).reset_index(drop=True)
    sorted_df.to_csv(BASE_DIR / "updated_sales.csv", index=False)

    # PART 4: Matplotlib charts
    currency = FuncFormatter(lambda x, pos: f"${x:,.0f}")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(product_revenue.index, product_revenue.values)
    ax.set_title("Total Revenue by Product", fontsize=15, pad=14)
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Revenue ($)")
    ax.yaxis.set_major_formatter(currency)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.bar_label(bars, labels=[f"${v:,.0f}" for v in product_revenue.values], padding=3, fontsize=9)
    ax.set_ylim(0, product_revenue.max() * 1.14)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "bar_chart.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.pie(
        category_revenue.values,
        labels=category_revenue.index,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.72,
        textprops={"fontsize": 11},
    )
    ax.set_title("Revenue Share by Category", fontsize=15, pad=18)
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(BASE_DIR / "pie_chart.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.hist(df["Total_Sales"], bins=8, edgecolor="white", linewidth=1.2)
    ax.set_title("Distribution of Sales Revenue per Record", fontsize=15, pad=14)
    ax.set_xlabel("Revenue per Sale ($)")
    ax.set_ylabel("Number of Sales Records")
    ax.xaxis.set_major_formatter(currency)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "histogram.png", dpi=180)
    plt.close(fig)

    # PART 5: Functions and interpretation (generated from the dataset)
    analysis = (
        "HW 7 - Sales Data Analysis\n"

        f"Dataset: {len(df)} sales records, {df['Product'].nunique()} products, "

        f"{df['Category'].nunique()} categories, {df['Region'].nunique()} regions.\n"
       
        f"Total revenue: ${total_revenue:,.2f}\n"
       
        f"Total quantity sold: {int(np.sum(quantities))} items\n\n"
       
       "1. Which product generated the highest revenue?\n"
       
        f"{top_product}, with ${top_product_revenue:,.2f} in combined revenue.\n\n"
       
        "2. Which category generated the most revenue?\n"
       
        f"{top_category}, with ${category_revenue.iloc[0]:,.2f} in revenue "
       
        f"({category_revenue.iloc[0] / total_revenue * 100:.1f}% of the total).\n\n"
       
        "3. Which region performed best?\n"
      
        f"{top_region}, with ${region_revenue.iloc[0]:,.2f} in revenue.\n\n"
     
        "4. What can you conclude from your analysis?\n"
     
        f"Revenue is driven mainly by {top_category.lower()} products. "
      
        f"{top_product} is the strongest individual product, and {top_region} "
        "is the highest-revenue region.\n\n"
        
        
        "Revenue by product:\n"
        + "\n".join(f"- {name}: ${amount:,.2f}" for name, amount in product_revenue.items())
        + "\n\nRevenue by category:\n"
        + "\n".join(f"- {name}: ${amount:,.2f}" for name, amount in category_revenue.items())
        + "\n\nRevenue by region:\n"
        + "\n".join(f"- {name}: ${amount:,.2f}" for name, amount in region_revenue.items())
        + "\n"
    )
    (BASE_DIR / "analysis.txt").write_text(analysis, encoding="utf-8")
    print("\nPARTS 4 AND 5: Generated three chart PNGs and analysis.txt.")
    print("Saved updated_sales.csv, analysis.txt, bar_chart.png, pie_chart.png, histogram.png")


if __name__ == "__main__":
    main()
