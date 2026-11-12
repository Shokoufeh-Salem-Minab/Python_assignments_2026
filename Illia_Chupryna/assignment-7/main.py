import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_revenue(quantity, price):
    return quantity * price

def get_top_product(data):
    totals = data.groupby("Product")["Total_Sales"].sum()
    return totals.idxmax(), totals.max()

df = pd.read_csv("sales.csv")
products = df["Product"].tolist()
quantity_by_product = df.groupby("Product")["Quantity"].sum().to_dict()
quantities = np.array(df["Quantity"])

print("Products:", products)
print("Quantity by product:", quantity_by_product)
print("Total quantity:", np.sum(quantities))
print("Average quantity:", np.mean(quantities))
print("Maximum quantity:", np.max(quantities))
print("Minimum quantity:", np.min(quantities))
print("Standard deviation:", round(np.std(quantities), 2))
print("Indices where quantity > 5:", np.where(quantities > 5)[0])
print(df.head())
df.info()
print(df.describe())

df["Total_Sales"] = calculate_revenue(df["Quantity"], df["Price"])
print("Total revenue:", df["Total_Sales"].sum())
print("Top product:", get_top_product(df))
print("Revenue by category:")
print(df.groupby("Category")["Total_Sales"].sum())
print("Revenue by region:")
print(df.groupby("Region")["Total_Sales"].sum())
print(df.sort_values("Total_Sales", ascending=False))
df.to_csv("updated_sales.csv", index=False)

df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False).plot(kind="bar")
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("bar_chart.png")
plt.close()

df.groupby("Category")["Total_Sales"].sum().plot(kind="pie", autopct="%1.1f%%")
plt.title("Revenue by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig("pie_chart.png")
plt.close()

plt.hist(df["Total_Sales"], bins=8, edgecolor="black")
plt.title("Distribution of Sales Revenue")
plt.xlabel("Sales Revenue")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("histogram.png")
plt.close()
