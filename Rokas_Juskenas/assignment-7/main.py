import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rawData = {
    'Product': [
        "Laptop", 'Phone', "Headphones", 'Mouse', "Keyboard",
        "Laptop", 'Phone', "Headphones", 'Mouse', "Keyboard",
        "Laptop", 'Phone', "Headphones", 'Mouse', "Keyboard", 'Laptop'
    ],
    "Category": [
        'Electronics', "Electronics", 'Accessories', "Accessories", 'Accessories',
        "Electronics", 'Electronics', "Accessories", 'Accessories', "Accessories",
        'Electronics', "Electronics", 'Accessories', "Accessories", 'Accessories', "Electronics"
    ],
    'Quantity': [ 3, 7, 12, 15, 8, 4, 9, 6, 10, 5, 2, 8, 14, 11, 7, 5 ],
    "Price": [ 1000, 600, 150, 30, 50, 1050, 580, 140, 25, 55, 1100, 620, 150, 30, 50, 980 ],
    'Region': [
        'North', "South", 'East', "West", 'North',
        "South", 'East', "West", 'North', "South",
        'East', "West", 'North', "South", 'East', "West"
    ]
}

init_df = pd.DataFrame( rawData )
init_df.to_csv( "sales.csv" , index = False )
print( "PART 1: sales.csv made with " + str( len( init_df ) ) + " rows.\n" )


def get_top_product( df_data ):
    p_rev = df_data.groupby( 'Product' )[ "Total_Sales" ].sum()
    top_p = p_rev.idxmax()
    max_r = p_rev.max()
    return top_p , max_r

def calculate_revenue( q , p ):
    res = q * p
    return res


print( "--- PART 2: Python and NumPy Analysis ---" )

p_list = []
raw_prods = init_df[ 'Product' ]
for i in range( len( raw_prods ) ):
    p_list.append( raw_prods[ i ] )
print( "Product Names List:" , p_list )

tot_qty_dict = {}
grp_q = init_df.groupby( "Product" )[ 'Quantity' ].sum()
for p_name, q_val in grp_q.items():
    tot_qty_dict[ p_name ] = q_val
print( "Total Quantity Sold per Product: " + str( tot_qty_dict ) )

q_list = []
raw_q = init_df[ "Quantity" ]
for i in range( len( raw_q ) ):
    q_list.append( raw_q[ i ] )
quantities_arr = np.array( q_list )
print( f"Quantities NumPy Array: {quantities_arr}" )

tot_qty = 0
for i in range( len( quantities_arr ) ):
    tot_qty = tot_qty + quantities_arr[ i ]

avgQty = np.mean( quantities_arr )
max_qty = np.max( quantities_arr )
min_qty = np.min( quantities_arr )
std_qty = np.std( quantities_arr )

print( "Total Quantity Sold: %d" % tot_qty )
print( "Average Quantity Sold: " + f"{avgQty:.2f}" )
print( "Maximum Quantity Sold: " + str( max_qty ) )
print( "Minimum Quantity Sold: " + str( min_qty ) )
print( "Standard Deviation of Quantity: {:.2f}".format( std_qty ) )

gt5_list = []
for i in range( len( quantities_arr ) ):
    if quantities_arr[ i ] > 5:
        gt5_list.append( i )
indices_gt_5 = np.array( gt5_list )
print( "Indices where Quantity > 5:" , indices_gt_5 , "\n" )


print( "--- PART 3: Pandas Processing ---" )

df = pd.read_csv( 'sales.csv' )

print( "\n--- First 5 Rows ---" )
print( df.head() )

print( "\n--- Dataset Info ---" )
df.info()

print( "\n--- Descriptive Statistics ---" )
print( df.describe() )

df[ "Total_Sales" ] = calculate_revenue( df[ 'Quantity' ] , df[ "Price" ] )

tot_rev = df[ 'Total_Sales' ].sum()
print( "\nTotal Overall Revenue: $" + "%.2f" % tot_rev )

top_prod_name , top_prod_rev = get_top_product( df )
print( "Product with Highest Sales Revenue: " + top_prod_name + " ($" + f"{top_prod_rev:,.2f}" + ")" )

cat_rev = df.groupby( "Category" )[ 'Total_Sales' ].sum()
print( "\nTotal Revenue by Category:" )
print( cat_rev )

reg_sales = df.groupby( 'Region' )[ "Total_Sales" ].sum()
best_reg = reg_sales.idxmax()
best_reg_sales = reg_sales.max()
print( f"\nRegion with Highest Sales: {best_reg} (${best_reg_sales:,.2f})" )

df_sorted = df.sort_values( by = 'Total_Sales' , ascending = False )
print( "\n--- Sorted DataFrame (Top 5 Rows) ---" )
print( df_sorted.head() )

df_sorted.to_csv( "updated_sales.csv" , index = False )
print( "\nSaved updated dataset to 'updated_sales.csv'.\n" )


print( "--- PART 4: Generating Charts ---" )

if "seaborn-v0_8-whitegrid" in plt.style.available:
    plt.style.use( 'seaborn-v0_8-whitegrid' )
else:
    plt.style.use( 'default' )

prod_r = df.groupby( 'Product' )[ 'Total_Sales' ].sum().sort_values( ascending = False )
plt.figure( figsize = ( 8 , 5 ) )
plt.bar( prod_r.index , prod_r.values , color = 'teal' , edgecolor = "black" )
plt.title( "Total Revenue by Product" , fontsize = 14 , fontweight = 'bold' )
plt.xlabel( "Product Name" , fontsize = 12 )
plt.ylabel( "Total Revenue ($)" , fontsize = 12 )
plt.xticks( rotation = 15 )
plt.tight_layout()
plt.savefig( "bar_chart.png" , dpi = 300 )
plt.close()
print( "Saved 'bar_chart.png'" )

cat_r = df.groupby( "Category" )[ "Total_Sales" ].sum()
plt.figure( figsize = ( 7 , 7 ) )
plt.pie(
    cat_r.values ,
    labels = cat_r.index ,
    autopct = "%1.1f%%" ,
    startangle = 140 ,
    colors = [ '#4c72b0' , "#55a868" ] ,
    explode = ( 0.05 , 0 ) ,
    shadow = True
)
plt.title( "Revenue Share by Product Category" , fontsize = 14 , fontweight = "bold" )
plt.tight_layout()
plt.savefig( 'pie_chart.png' , dpi = 300 )
plt.close()
print( "Saved 'pie_chart.png'" )

plt.figure( figsize = ( 8 , 5 ) )
plt.hist( df[ "Total_Sales" ] , bins = 6 , color = "coral" , edgecolor = 'black' , alpha = 0.8 )
plt.title( "Distribution of Transaction Sales Revenue" , fontsize = 14 , fontweight = 'bold' )
plt.xlabel( "Sales Revenue per Transaction ($)" , fontsize = 12 )
plt.ylabel( "Frequency" , fontsize = 12 )
plt.tight_layout()
plt.savefig( 'histogram.png' , dpi = 300 )
plt.close()
print( "Saved 'histogram.png'\n" )


top_cat_name = cat_rev.idxmax()
top_cat_rev = cat_rev.max()

pct_electronics = ( cat_rev.max() / tot_rev ) * 100.0

analysis_txt = f"""Sales Data Analysis Summary
===========================

1. Which product generated the highest revenue?
Answer: {top_prod_name} made the most total revenue with ${top_prod_rev:,.2f}.

2. Which category generated the most revenue?
Answer: The {top_cat_name} category made the most money overall, which came out to ${top_cat_rev:,.2f}.

3. Which region performed best?
Answer: The {best_reg} region had the best performance with total sales of ${best_reg_sales:,.2f}.

4. What can you conclude from your analysis?
Conclusion:
- Expensive tech items like Phones and Laptops bring in almost all of the money ({pct_electronics:.1f}% of overall revenue comes from {top_cat_name}), even though people buy fewer of them compared to cheaper accessories.
- Cheaper accessories like Mice, Keyboards, and Headphones sell a lot of items (high quantity sold) and are good add-on buys, but they don't bring in anywhere near as much gross revenue because the unit price is low.
- Sales are pretty different depending on the region, and the {best_reg} region made the most money out of all the areas.
- Recommendation: The store should try to bundle accessories together with expensive devices when selling in top regions like {best_reg} so customers spend more per order.
"""

f_out = open( "analysis.txt" , "w" )
f_out.write( analysis_txt )
f_out.close()

print( "Saved interpretation text to 'analysis.txt'." )
print( "Execution complete. All deliverables generated." )