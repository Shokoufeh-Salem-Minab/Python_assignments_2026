
import os
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# functions

def calculate_revenue(quantity, price):
    """Return total revenue = quantity * price"""
    return quantity * price


def get_top_products(df):
    """Return (product, revenue) for the product with the highest total revenue"""
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum()
    return revenue_by_product.idxmax(), revenue_by_product.max()


# csv file

print("=" * 60, "\nQuestion 2\n", "=" * 60, sep="")

products, quantities_list = [], []

with open("sales.csv", newline="") as f:
    for row in csv.DictReader(f):
        products.append(row["Product"])
        quantities_list.append(int(row["Quantity"]))

print("Product list:", products)

qty_by_product = {}

for p, q in zip(products, quantities_list):
    qty_by_product[p] = qty_by_product.get(p, 0) + q

print("Total quantity per product:", qty_by_product)

quantities = np.array(quantities_list)

print("Quantities array:", quantities)
print("Total quantity sold :", quantities.sum())
print("Average quantity    :", round(quantities.mean(), 2))
print("Maximum quantity    :", quantities.max())
print("Minimum quantity    :", quantities.min())
print("Standard deviation  :", round(quantities.std(), 2))

idx = np.where(quantities > 5)[0]

print("Indices with quantity > 5:", idx)
print("Products at those indices:", [products[i] for i in idx])


# pandas

print("\n" + "=" * 60, "\nQuestion 3\n", "=" * 60, sep="")

df = pd.read_csv("sales.csv")

print("\n1. First 5 rows:\n", df.head())

print("\n2. Info:")
df.info()

print("\n3. Describe:\n", df.describe())

df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])

print("\n4. Total_Sales column added:\n", df.head())

total_revenue = df["Total_Sales"].sum()

print(f"\n5. Total revenue: ${total_revenue:,.2f}")

top_product, top_product_rev = get_top_products(df)

print(f"6. Top product: {top_product} (${top_product_rev:,.2f})")

category_revenue = df.groupby("Category")["Total_Sales"].sum()

print("\n7. Revenue by category:\n", category_revenue)

region_revenue = df.groupby("Region")["Total_Sales"].sum()

print("\n8. Revenue by region:\n", region_revenue)

top_region = region_revenue.idxmax()

print("   Best region:", top_region)

df_sorted = df.sort_values("Total_Sales", ascending=False)

print("\n9. Sorted by Total_Sales (desc):\n", df_sorted)

df_sorted.to_csv("updated_sales.csv", index=False)

print("\n10. Saved updated_sales.csv")


# visualization

product_revenue = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)


# bar chart

plt.figure(figsize=(8, 5))

bars = plt.bar(
    product_revenue.index,
    product_revenue.values,
    color="steelblue",
    edgecolor="black"
)

plt.bar_label(
    bars,
    labels=[f"${v:,.0f}" for v in product_revenue.values],
    padding=3
)

plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue ($)")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("bar_chart.png", dpi=150)
plt.close()


# pie chart

plt.figure(figsize=(7, 7))

plt.pie(
    category_revenue.values,
    labels=category_revenue.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "white"}
)

plt.title("Share of Total Revenue by Category")
plt.tight_layout()
plt.savefig("pie_chart.png", dpi=150)
plt.close()


# histogram

plt.figure(figsize=(8, 5))

plt.hist(
    df["Total_Sales"],
    bins=6,
    color="seagreen",
    edgecolor="black"
)

plt.title("Distribution of Sales Revenue per Transaction")
plt.xlabel("Sales Revenue ($)")
plt.ylabel("Number of Transactions")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.close()

print("\nCharts saved: bar_chart.png, pie_chart.png, histogram.png")


# analysis

top_cat = category_revenue.idxmax()
cat_share = category_revenue.max() / total_revenue * 100

with open("analysis.txt", "w") as f:

    f.write("Sales Data Analysis\n===================\n\n")

    f.write(
        f"1. Which product generated the highest revenue?\n"
        f"   {top_product}, with ${top_product_rev:,.2f}.\n\n"
    )

    f.write(
        f"2. Which category generated the most revenue?\n"
        f"   {top_cat}, with ${category_revenue.max():,.2f} "
        f"({cat_share:.1f}% of total revenue).\n\n"
    )

    f.write(
        f"3. Which region performed best?\n"
        f"   {top_region}, with ${region_revenue.max():,.2f}.\n\n"
    )

    f.write("4. What can you conclude from your analysis?\n")

    f.write(
        "Revenue is mostly impacted by price, not the volume of items sold. "
        "Mice sold the most units (46) but generated the least revenue, "
        "while Phones sold only 28 units but generated the most revenue.\n\n"
    )

    f.write(
        "Phones and Laptops together account for about 87% of total revenue, "
        "even though they make up only 30% of the total units sold.\n\n"
    )

    f.write(
        "Accessories (Mouse, Keyboard, Headphones) are high-volume but "
        "low-value products because they have high unit sales but generate "
        "relatively low revenue.\n\n"
    )

    f.write(
        "The East, South and West regions have relatively similar revenue, "
        "but the West is the weakest-performing region.\n\n"
    )

    f.write(
        "Based on the histogram, the distribution of revenue per transaction "
        "appears to be skewed to the right because a few high-value sales "
        "increase the overall revenue.\n\n"
    )

    f.write(
        "A limitation is that the dataset contains only 18 records, "
        "so the conclusions are indicative rather than statistically "
        "conclusive.\n"
    )

print("analysis.txt written")
