"""
Python Data Analysis
Sales Data Analysis
"""

import csv
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt



# Part 5 - Function
def calculate_revenue(quantity, price):
    """Return total revenue for a given quantity and price."""
    return quantity * price


def get_top_product(df):
    """Return (product_name, revenue) of the product with the highest total revenue."""
    revenue_by_product = df.groupby("Product")["Total_Sales"].sum()
    return revenue_by_product.idxmax(), revenue_by_product.max()


# Part 2 - Python and NumPy
print("=" * 60)
print("PART 2 - PYTHON AND NUMPY")
print("=" * 60)

products = []
quantities = []
with open("sales.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append(row["Product"])
        quantities.append(int(row["Quantity"]))

print("Product list:", products)

# Dictionary: total quantity sold per product
quantity_per_product = {}
for product, qty in zip(products, quantities):
    quantity_per_product[product] = quantity_per_product.get(product, 0) + qty
print("\nTotal quantity per product:", quantity_per_product)

# NumPy array of all quantities
qty_array = np.array(quantities)
print("\nQuantities array:", qty_array)

print("Total quantity sold  :", qty_array.sum())
print("Average quantity sold:", round(qty_array.mean(), 2))
print("Maximum quantity     :", qty_array.max())
print("Minimum quantity     :", qty_array.min())
print("Standard deviation   :", round(qty_array.std(), 2))

# Indices of records where quantity sold is greater than 5
indices = np.where(qty_array > 5)[0]
print("\nIndices where quantity > 5:", indices)
print("Products at those indices :", [products[i] for i in indices])



# Part 3 - Pandas
print("\n" + "=" * 60)
print("PART 3 - PANDAS")
print("=" * 60)

df = pd.read_csv("sales.csv")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset info:")
df.info()

print("\nDescriptive statistics:")
print(df.describe())

# New column
df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])

total_revenue = df["Total_Sales"].sum()
print(f"\nTotal revenue: ${total_revenue:,.2f}")

top_product, top_product_revenue = get_top_product(df)
print(f"Product with highest revenue: {top_product} (${top_product_revenue:,.2f})")

revenue_by_product = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
print("\nRevenue by product:")
print(revenue_by_product)

revenue_by_category = df.groupby("Category")["Total_Sales"].sum().sort_values(ascending=False)
print("\nRevenue by category:")
print(revenue_by_category)

revenue_by_region = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
print("\nRevenue by region:")
print(revenue_by_region)
best_region = revenue_by_region.idxmax()
print(f"\nRegion with highest sales: {best_region} (${revenue_by_region.max():,.2f})")

df_sorted = df.sort_values(by="Total_Sales", ascending=False)
print("\nDataFrame sorted by Total_Sales (descending):")
print(df_sorted)

df_sorted.to_csv("updated_sales.csv", index=False)
print("\nSaved updated_sales.csv")


# Part 4 - Data Visualization
print("\n" + "=" * 60)
print("PART 4 - VISUALIZATION")
print("=" * 60)

# 1. Bar chart - revenue per product
plt.figure(figsize=(8, 5))
bars = plt.bar(revenue_by_product.index, revenue_by_product.values,
               color=["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"])
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Total Revenue ($)")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("bar_chart_revenue_by_product.png", dpi=150)
plt.close()

# 2. Pie chart - revenue share per category
plt.figure(figsize=(7, 7))
plt.pie(revenue_by_category.values, labels=revenue_by_category.index,
        autopct="%1.1f%%", startangle=90,
        colors=["#4C72B0", "#55A868", "#C44E52"],
        wedgeprops={"edgecolor": "white"})
plt.title("Percentage of Total Revenue by Category")
plt.tight_layout()
plt.savefig("pie_chart_revenue_by_category.png", dpi=150)
plt.close()

# 3. Histogram - distribution of sales revenue
plt.figure(figsize=(8, 5))
plt.hist(df["Total_Sales"], bins=8, color="#4C72B0", edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Revenue per Sale ($)")
plt.ylabel("Number of Sales")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("histogram_sales_revenue.png", dpi=150)
plt.close()

print("Saved 3 charts.")


# Part 5 - Write analysis.txt
top_category = revenue_by_category.idxmax()
cat_share = revenue_by_category.max() / total_revenue * 100
region_share = revenue_by_region.max() / total_revenue * 100
low_product = revenue_by_product.idxmin()
top_qty_product = max(quantity_per_product, key=quantity_per_product.get)

analysis = f"""SALES DATA ANALYSIS - ANSWERS

1. Which product generated the highest revenue?
   {top_product} generated the highest revenue: ${top_product_revenue:,.2f}
   ({top_product_revenue / total_revenue * 100:.1f}% of total revenue of ${total_revenue:,.2f}).

2. Which category generated the most revenue?
   The {top_category} category generated the most revenue: ${revenue_by_category.max():,.2f}
   ({cat_share:.1f}% of total revenue).

3. Which region performed best?
   The {best_region} region performed best with ${revenue_by_region.max():,.2f}
   in sales ({region_share:.1f}% of total revenue).

4. What can you conclude from your analysis?
   - High-priced products drive revenue more than high volume. {top_product} was not the
     best-selling item by units, yet it earned the most because of its high price.
   - {top_qty_product} sold the most units ({quantity_per_product[top_qty_product]}), but because it is cheap it
     contributes little revenue. {low_product} earned the least revenue overall (${revenue_by_product.min():,.2f}).
   - The {top_category} category is the main source of income, so the business should
     keep strong stock and promotion for these products.
   - Revenue is spread across all regions, but {best_region} leads. Weaker regions could be
     targeted with marketing or promotions.
   - Most individual sales are small (low revenue per record), with a few large sales
     (Laptops and Phones) pulling the total up, as seen in the histogram.
"""

with open("analysis.txt", "w") as f:
    f.write(analysis)
print("Saved analysis.txt")
