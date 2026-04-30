import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("🛒 Sales Data Analysis Dashboard")

st.write("Upload your E-commerce CSV file")

# Upload file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if not uploaded_file:
    st.info("Please upload a dataset")
    st.stop()

# Load data
df = pd.read_csv(uploaded_file)

# Clean data
df = df.dropna()

# Create Total Sales column
if "Price" in df.columns and "Quantity" in df.columns:
    df["TotalSales"] = df["Price"] * df["Quantity"]

# ---------------------------
# 📊 Preview
# ---------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# ---------------------------
# 📈 Summary
# ---------------------------
st.subheader("📈 Summary Statistics")
st.write(df.describe())

# ---------------------------
# 🏆 Top Products
# ---------------------------
if "Product" in df.columns:
    st.subheader("🏆 Top Products")
    top_products = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
    st.write(top_products)

    fig1, ax1 = plt.subplots()
    top_products.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

# ---------------------------
# 📦 Category Analysis
# ---------------------------
if "Category" in df.columns:
    st.subheader("📦 Category Sales")
    category_sales = df.groupby("Category")["TotalSales"].sum()
    st.write(category_sales)

    fig2, ax2 = plt.subplots()
    category_sales.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    st.pyplot(fig2)

# ---------------------------
# 🌆 City Analysis
# ---------------------------
if "City" in df.columns:
    st.subheader("🌆 City-wise Sales")
    city_sales = df.groupby("City")["TotalSales"].sum()
    st.write(city_sales)

# ---------------------------
# 👥 Customer Analysis
# ---------------------------
if "CustomerID" in df.columns:
    st.subheader("👥 Top Customers")
    customer_spending = df.groupby("CustomerID")["TotalSales"].sum().sort_values(ascending=False)
    st.write(customer_spending.head())

# ---------------------------
# 🔢 NumPy Analysis
# ---------------------------
if "TotalSales" in df.columns:
    sales_array = df["TotalSales"].to_numpy()

    st.subheader("🔢 NumPy Analysis")
    st.write("Mean Sales:", np.mean(sales_array))
    st.write("Total Sales:", np.sum(sales_array))

# ---------------------------
# 📊 Correlation
# ---------------------------
numeric_cols = df.select_dtypes(include=np.number)

if len(numeric_cols.columns) > 1:
    st.subheader("📊 Correlation Matrix")
    st.write(numeric_cols.corr())