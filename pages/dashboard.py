import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# SECURITY CHECK
# -------------------------
if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("login.py")

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# -------------------------
# TITLE
# -------------------------
st.title("🛒 Sales Data Analysis Dashboard")

st.success(
    f"Welcome {st.session_state.user}"
)

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if not uploaded_file:
    st.info("Please upload dataset")
    st.stop()

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(uploaded_file)

df = df.dropna()

# -------------------------
# TOTAL SALES
# -------------------------
if "Price" in df.columns and "Quantity" in df.columns:
    df["TotalSales"] = (
        df["Price"] * df["Quantity"]
    )

# -------------------------
# PREVIEW
# -------------------------
st.subheader("📊 Dataset Preview")

st.dataframe(df.head())

# -------------------------
# SUMMARY
# -------------------------
st.subheader("📈 Summary Statistics")

st.write(df.describe())

# -------------------------
# TOP PRODUCTS
# -------------------------
if "Product" in df.columns:

    st.subheader("🏆 Top Products")

    top_products = (
        df.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    st.write(top_products)

    fig1, ax1 = plt.subplots()

    top_products.plot(
        kind="bar",
        ax=ax1
    )

    st.pyplot(fig1)

# -------------------------
# CATEGORY ANALYSIS
# -------------------------
if "Category" in df.columns:

    st.subheader("📦 Category Sales")

    category_sales = (
        df.groupby("Category")["TotalSales"]
        .sum()
    )

    st.write(category_sales)

    fig2, ax2 = plt.subplots()

    category_sales.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax2
    )

    st.pyplot(fig2)

# -------------------------
# CITY ANALYSIS
# -------------------------
if "City" in df.columns:

    st.subheader("🌆 City-wise Sales")

    city_sales = (
        df.groupby("City")["TotalSales"]
        .sum()
    )

    st.write(city_sales)

# -------------------------
# CUSTOMER ANALYSIS
# -------------------------
if "CustomerID" in df.columns:

    st.subheader("👥 Top Customers")

    customer_spending = (
        df.groupby("CustomerID")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.write(customer_spending.head())

# -------------------------
# NUMPY ANALYSIS
# -------------------------
if "TotalSales" in df.columns:

    sales_array = df["TotalSales"].to_numpy()

    st.subheader("🔢 NumPy Analysis")

    st.write(
        "Mean Sales:",
        np.mean(sales_array)
    )

    st.write(
        "Total Sales:",
        np.sum(sales_array)
    )

# -------------------------
# CORRELATION
# -------------------------
numeric_cols = df.select_dtypes(
    include=np.number
)

if len(numeric_cols.columns) > 1:

    st.subheader("📊 Correlation Matrix")

    st.write(numeric_cols.corr())

# -------------------------
# LOGOUT
# -------------------------
if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.switch_page("login.py")