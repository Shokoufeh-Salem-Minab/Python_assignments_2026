import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_revenue(quantity, price):
    """Calculate revenue from quantity and price."""
    return quantity * price


def get_top_product(data):
    """Return the product with the highest total revenue."""
    revenue = data.groupby("Product")["Total_Sales"].sum()
    return revenue.idxmax()


def main():
    # Read the CSV file
    data = pd.read_csv("sales.csv")

    # PART 2 - PYTHON AND NUMPY
    product_names = data["Product"].tolist()
    print("Product names:", product_names)

    quantity_dictionary = data.groupby("Product")["Quantity"].sum().to_dict()
    print("Total quantity by product:", quantity_dictionary)

    quantities = np.array(data["Quantity"])
    print("Quantities:", quantities)
    print("Total quantity:", np.sum(quantities))
    print("Average quantity:", np.mean(quantities))
    print("Maximum quantity:", np.max(quantities))
    print("Minimum quantity:", np.min(quantities))
    print("Standard deviation:", np.std(quantities))

    indices = np.where(quantities > 5)[0]
    print("Indices where quantity is greater than 5:", indices)

    # PART 3 - PANDAS
    print("\nFirst 5 rows:")
    print(data.head())

    print("\nDataset information:")
    data.info()

    print("\nDescriptive statistics:")
    print(data.describe())

    data["Total_Sales"] = data["Quantity"] * data["Price"]
    total_revenue = data["Total_Sales"].sum()
    print("\nTotal revenue:", total_revenue)

    product_revenue = data.groupby("Product")["Total_Sales"].sum()
    print("\nRevenue by product:")
    print(product_revenue)
    print("Top product:", get_top_product(data))

    category_revenue = data.groupby("Category")["Total_Sales"].sum()
    print("\nRevenue by category:")
    print(category_revenue)

    region_revenue = data.groupby("Region")["Total_Sales"].sum()
    best_region = region_revenue.idxmax()
    print("\nRevenue by region:")
    print(region_revenue)
    print("Best region:", best_region)

    sorted_data = data.sort_values("Total_Sales", ascending=False)
    sorted_data.to_csv("updated_sales.csv", index=False)
    print("\nSaved updated_sales.csv")

    # PART 4 - MATPLOTLIB
    product_revenue.sort_values(ascending=False).plot(kind="bar")
    plt.title("Total Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("bar_chart.png")
    plt.show()
    plt.close()

    category_revenue.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Revenue Share by Category")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("pie_chart.png")
    plt.show()
    plt.close()

    plt.hist(data["Total_Sales"], bins=8, edgecolor="black")
    plt.title("Distribution of Sales Revenue")
    plt.xlabel("Sales Revenue")
    plt.ylabel("Number of Sales Records")
    plt.tight_layout()
    plt.savefig("histogram.png")
    plt.show()
    plt.close()

    # PART 5 - FUNCTIONS AND INTERPRETATION
    print("\nExample calculate_revenue(3, 100):", calculate_revenue(3, 100))
    top_product = get_top_product(data)
    top_category = category_revenue.idxmax()
    top_region = region_revenue.idxmax()

    report = f"""HOMEWORK 7 - SALES DATA ANALYSIS

1. Product with the highest revenue:
{top_product} - {product_revenue.max():.2f}

2. Category with the highest revenue:
{top_category} - {category_revenue.max():.2f}

3. Region with the highest revenue:
{top_region} - {region_revenue.max():.2f}

4. Conclusion:
The dataset contains {len(data)} sales records. Total revenue is {total_revenue:.2f}.
{top_product} generated the highest revenue, {top_category} was the strongest
category, and {top_region} was the best-performing region. The charts make it
easier to compare product revenue, category shares and individual sale values.
"""
    with open("analysis.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print("Saved analysis.txt")
    print("Homework 7 completed.")


if __name__ == "__main__":
    main()
