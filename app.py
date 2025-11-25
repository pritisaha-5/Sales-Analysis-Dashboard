import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

# ------------------- Page Setup -------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard")

# ------------------ Database Connection ------------------
st.sidebar.header("Database Connection")

# Use raw string or double backslash for server name
server = st.sidebar.text_input("Server", r"localhost\SQLEXPRESS")
database = st.sidebar.text_input("Database", "SalesDB")

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

# Test connection with detailed error messages
try:
    conn = pyodbc.connect(conn_str, timeout=5)
    st.success(f"Connected to SQL Server at {server} successfully!")
except Exception as e:
    st.error(
        f"Connection failed!\n\n"
        "Please check the following:\n"
        "1. SQL Server service is running.\n"
        "2. TCP/IP is enabled in SQL Server Configuration Manager.\n"
        "3. Firewall allows inbound connections on TCP port 1433.\n"
        "4. You are using the correct server name and instance.\n\n"
        f"Error details:\n{e}"
    )
    st.stop()  # Stop the app if connection fails

# ------------------ Load Data ------------------
query = "SELECT * FROM MyTable;"
try:
    df = pd.read_sql(query, conn)
except Exception as e:
    st.error(f"Failed to load data from table 'MyTable'.\nError: {e}")
    st.stop()

# ------------------ Clean Data ------------------
df.columns = df.columns.str.strip().str.replace(" ", "_")
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df = df.dropna()

# ------------------ Key Metrics ------------------
st.header("Key Metrics")
total_sales = df['Total_Amount'].sum()
avg_order_value = df['Total_Amount'].mean()
total_customers = df['Customer_ID'].nunique()
repeat_customers = df['Customer_ID'].value_counts()
repeat_customers = repeat_customers[repeat_customers > 1].count()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Average Order Value", f"${avg_order_value:,.2f}")
col3.metric("Total Customers", total_customers)
col4.metric("Repeat Customers", repeat_customers)

# ------------------ Monthly Sales ------------------
st.header("Monthly Sales Trend")
df['Month'] = df['Order_Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Total_Amount'].sum()
fig, ax = plt.subplots(figsize=(10,5))
monthly_sales.plot(ax=ax, title="Monthly Sales Trend")
st.pyplot(fig)

# ------------------ Top Products ------------------
st.header("Top 10 Products")
top_products = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)

# ------------------ Regional Performance ------------------
st.header("Sales by Region")
region_perf = df.groupby('Region')['Total_Amount'].sum()
st.bar_chart(region_perf)

# ------------------ ABC Analysis ------------------
st.header("ABC Analysis")
df_product = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False)
cum_percent = df_product.cumsum() / df_product.sum() * 100
ABC = pd.cut(cum_percent, bins=[0, 80, 95, 100], labels=['A','B','C'])
abc_df = pd.DataFrame({"Sales": df_product, "Class": ABC})
st.dataframe(abc_df.head(15))
