import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Sales Analysis Dashboard")

st.sidebar.header("Upload Sales CSV File")
uploaded_file = st.sidebar.file_uploader("Upload your sales data CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert date if present
    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')

    st.subheader("Preview of Data")
    st.write(df.head())

    # ------------------ KPIs ------------------
    if 'Total_Amount' in df.columns and 'Customer_ID' in df.columns:
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

    # ------------------ Monthly Sales Trend ------------------
    if 'Order_Date' in df.columns and 'Total_Amount' in df.columns:
        st.header("Monthly Sales Trend")
        df['Month'] = df['Order_Date'].dt.to_period('M')
        monthly_sales = df.groupby('Month')['Total_Amount'].sum()

        fig, ax = plt.subplots(figsize=(10, 5))
        monthly_sales.plot(ax=ax, title="Monthly Sales Trend")
        st.pyplot(fig)

    # ------------------ Top Products ------------------
    if 'Product_Name' in df.columns and 'Total_Amount' in df.columns:
        st.header("Top 10 Products")
        top_products = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_products)

    # ------------------ Regional Performance ------------------
    if 'Region' in df.columns and 'Total_Amount' in df.columns:
        st.header("Sales by Region")
        region_perf = df.groupby('Region')['Total_Amount'].sum()
        st.bar_chart(region_perf)

    # ------------------ ABC Analysis ------------------
    if 'Product_Name' in df.columns and 'Total_Amount' in df.columns:
        st.header("ABC Analysis")
        df_product = df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False)
        cum_percent = df_product.cumsum() / df_product.sum() * 100
        ABC = pd.cut(cum_percent, bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])
        abc_df = pd.DataFrame({"Sales": df_product, "Class": ABC})
        st.dataframe(abc_df.head(15))

else:
    st.info("Upload a CSV file to start analysis.")
