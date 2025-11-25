# %%
import pyodbc

server = r"LAPTOP-RO8RV296\SQLEXPRESS"
database = "SalesDB"

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Connected Successfully!")
except Exception as e:
    print("Connection failed:", e)


# %%
import pandas as pd

query = "SELECT * FROM MyTable;"
df = pd.read_sql(query, conn)

df.head()


# %%
# Fix column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Convert dates
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Remove nulls if any
df = df.dropna()

df.info()


# %%
total_sales = df['Total_Amount'].sum()
avg_order_value = df['Total_Amount'].mean()
total_customers = df['Customer_ID'].nunique()

repeat_customers = df['Customer_ID'].value_counts()
repeat_customers = repeat_customers[repeat_customers > 1].count()

print("Total Sales:", total_sales)
print("Average Order Value:", avg_order_value)
print("Total Customers:", total_customers)
print("Repeat Customers:", repeat_customers)


# %%
df['Month'] = df['Order_Date'].dt.to_period('M')

monthly_sales = df.groupby('Month')['Total_Amount'].sum()

monthly_sales.plot(figsize=(10,5), title="Monthly Sales Trend")


# %%
top_products = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False).head(10)
top_products


# %%
top_products = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False).head(10)
top_products


# %%
region_perf = df.groupby('Region')['Total_Amount'].sum()
region_perf


# %%
df_product = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False)

cum_percent = df_product.cumsum() / df_product.sum() * 100

ABC = pd.cut(
    cum_percent,
    bins=[0, 80, 95, 100],
    labels=['A', 'B', 'C']
)

abc_df = pd.DataFrame({"Sales": df_product, "Class": ABC})
abc_df.head(15)


# %%
df = pd.read_sql(query, conn)

# %%
df.head()


# %%



