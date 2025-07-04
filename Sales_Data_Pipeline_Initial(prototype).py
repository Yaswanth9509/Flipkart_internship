import pandas as pd
import json
import os
from datetime import datetime

# TODO: try to make add some visualizations and powerful insights ( REMEMBER to copy this code )

print("Starting my data pipeline project...")
print("Checking for requirements to run the code...!")
# CSV Region
def load_csv_file(filename):
    # make sure csv file path is perfectly added
    if not os.path.exists(filename):
        print(f"Uh oh, can't find {filename}")
        return None
    try:
        df = pd.read_csv(filename)
        print(f"Got {len(df)} rows from {filename}")
        return df
    except:
        print(f"Something went wrong loading {filename}")
        return None
# JSON Region
def load_json_stuff(filename):
    # json file is added here to the code 
    if not os.path.exists(filename):
        print(f"Missing file: {filename}")
        return None    
    try:
        with open(filename) as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"JSON loaded - got {len(df)} products")
        return df
    except Exception as e:
        print(f"JSON failed: {e}")
        return None
#XLSX Region
def get_excel_data(filename):
    if not os.path.exists(filename):
        print(f"No excel file found: {filename}")
        return None
    try:
        df = pd.read_excel(filename)
        print(f"Excel loaded: {len(df)} regions")
        return df
    except:
        print("Excel loading failed")
        return None

# Data loading part
print("\n=== Loading Data ===")
sales_data = load_csv_file('sales_data.csv')
product_info = load_json_stuff('product_metadata.json')
region_data = get_excel_data('region_info.xlsx')

# check if everything loaded 
if sales_data is None or product_info is None or region_data is None:
    print("Some files didn't load properly :(")
    exit()

# Data merging area 
print("\n..........Combining Data..........")
# merge step 1
print("Merging sales with product info...")
step1 = pd.merge(sales_data, product_info, on='Product', how='left')
print(f"After merge 1: {len(step1)} records")
# merge step 2  
print("Adding region data...")
final_data = pd.merge(step1, region_data, on='Region', how='left')
print(f"Final dataset: {len(final_data)} records")

# check for any errors or missing statements after merging
missing = final_data.isnull().sum()
if missing.any():
    print("Warning: some data is missing after merging")
    print(missing[missing > 0])

print("\n=== Analysis Time ===")
# group by region and category ( basic )
revenue_summary = final_data.groupby(['Region', 'Category'])['Revenue'].sum().reset_index()
revenue_summary = revenue_summary.sort_values('Revenue', ascending=False)

print("Revenue by Region and Category:")
print("-" * 40)
for i, row in revenue_summary.iterrows():
    print(f"{row['Region']} - {row['Category']}: ${row['Revenue']:,.2f}")

# some extra analysis because why not
print("\n=== Extra Stats ===")
total_rev = final_data['Revenue'].sum()
avg_rev = final_data['Revenue'].mean()
best_region = final_data.groupby('Region')['Revenue'].sum().idxmax()
best_region_rev = final_data.groupby('Region')['Revenue'].sum().max()

print(f"Total Revenue: ${total_rev:,.2f}")
print(f"Average Revenue: ${avg_rev:.2f}")
print(f"Best Region: {best_region} (${best_region_rev:,.2f})")
print(f"Total Records Processed: {len(final_data)}")

# show top 5 individual sales
print("\nTop 5 Individual Sales:")
top_sales = final_data.nlargest(5, 'Revenue')[['Product', 'Region', 'Revenue']]
for i, row in top_sales.iterrows():
    print(f"  {row['Product']} in {row['Region']}: ${row['Revenue']:,.2f}")

print("\nDone! Pipeline finished successfully.")
print("This was actually easier than I thought it would be")