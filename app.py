import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------
# LOGIN PAGE
# -------------------------
if not st.session_state.logged_in:

    st.title("🔐 Login Page")

    email = st.text_input("Enter Gmail")
    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Login with Google"):

        # Demo Login
        if (
            email.endswith("@gmail.com")
            and password == "1234"
        ):

            st.session_state.logged_in = True

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Gmail or Password"
            )

    st.stop()

# =====================================================
# DASHBOARD
# =====================================================

st.title("🛒 Sales Data Analysis Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if not uploaded_file:

    st.info("Please upload dataset")
    st.stop()

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(uploaded_file)
# -------------------------
# RENAME COLUMNS
# -------------------------
df = df.rename(columns={
    "Product Name": "Product",
    "Product Category": "Category",
    "Units Sold": "Quantity",
    "Total Revenue": "TotalSales"
})
# -------------------------
# CLEAN DATA
# -------------------------
df = df.dropna()

# -------------------------
# TOTAL SALES
# -------------------------
if (
    "Price" in df.columns
    and "Quantity" in df.columns
):

    df["TotalSales"] = (
        df["Price"] * df["Quantity"]
    )

# -------------------------
# DATASET PREVIEW
# -------------------------
st.subheader("📊 Dataset Preview")

st.dataframe(df.head())

# -------------------------
# SUMMARY STATISTICS
# -------------------------
st.subheader("📈 Summary Statistics")

st.write(df.describe())

# -------------------------
# TOP PRODUCTS
# -------------------------
if "Product" in df.columns:

    st.subheader("🏆 Top Products")

    product_sales = (
        df.groupby("Product")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.write(product_sales)

# -------------------------
# CATEGORY SALES
# -------------------------
if "Category" in df.columns:

    st.subheader("📦 Category Sales")

    category_sales = (
        df.groupby("Category")["TotalSales"]
        .sum()
    )

    st.write(category_sales)

# -------------------------
# CITY SALES
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

    st.subheader("🔢 NumPy Analysis")

    sales_array = (
        df["TotalSales"]
        .to_numpy()
    )

    st.write(
        "Mean Sales:",
        np.mean(sales_array)
    )

    st.write(
        "Total Sales:",
        np.sum(sales_array)
    )

# -------------------------
# CORRELATION MATRIX
# -------------------------
numeric_cols = df.select_dtypes(
    include=np.number
)

if len(numeric_cols.columns) > 1:

    st.subheader("📊 Correlation Matrix")

    st.write(
        numeric_cols.corr()
    )

# =====================================================
# VISUALIZATIONS
# =====================================================

st.subheader("📊 Sales Visualizations")

# -------------------------
# BAR CHART
# -------------------------
if "Product" in df.columns:

    st.write("### 📦 Bar Chart")

    fig_bar, ax_bar = plt.subplots()

    product_sales.plot(
        kind="bar",
        ax=ax_bar
    )

    ax_bar.set_xlabel("Products")
    ax_bar.set_ylabel("Sales")
    ax_bar.set_title("Product Sales")

    st.pyplot(fig_bar)

# -------------------------
# LINE CHART
# -------------------------
if "Product" in df.columns:

    st.write("### 📈 Line Chart")

    fig_line, ax_line = plt.subplots()

    product_sales.plot(
        kind="line",
        marker="o",
        ax=ax_line
    )

    ax_line.set_xlabel("Products")
    ax_line.set_ylabel("Sales")
    ax_line.set_title("Sales Trend")

    st.pyplot(fig_line)

# -------------------------
# HISTOGRAM
# -------------------------
if "TotalSales" in df.columns:

    st.write("### 📊 Histogram")

    fig_hist, ax_hist = plt.subplots()

    ax_hist.hist(
        df["TotalSales"],
        bins=10
    )

    ax_hist.set_xlabel("Sales")
    ax_hist.set_ylabel("Frequency")
    ax_hist.set_title(
        "Sales Distribution"
    )

    st.pyplot(fig_hist)

# -------------------------
# PIE CHART
# -------------------------
if "Category" in df.columns:

    st.write("### 🥧 Pie Chart")

    fig_pie, ax_pie = plt.subplots()

    ax_pie.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%"
    )

    ax_pie.set_title(
        "Category Sales"
    )

    st.pyplot(fig_pie)

# -------------------------
# SCATTER PLOT
# -------------------------
if (
    "Price" in df.columns
    and "Quantity" in df.columns
):

    st.write("### 🔵 Scatter Plot")

    fig_scatter, ax_scatter = plt.subplots()

    ax_scatter.scatter(
        df["Price"],
        df["Quantity"]
    )

    ax_scatter.set_xlabel("Price")
    ax_scatter.set_ylabel("Quantity")
    ax_scatter.set_title(
        "Price vs Quantity"
    )

    st.pyplot(fig_scatter)

# -------------------------
# BOX PLOT
# -------------------------
if "TotalSales" in df.columns:

    st.write("### 📦 Box Plot")

    fig_box, ax_box = plt.subplots()

    ax_box.boxplot(
        df["TotalSales"]
    )

    ax_box.set_title(
        "Sales Spread"
    )

    st.pyplot(fig_box)

# -------------------------
# LOGOUT
# -------------------------
if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()