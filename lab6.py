import streamlit as st
import pandas as pd

# 1. PAGE CONFIGURATION AND DATASET

st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Load dataset
df = pd.read_csv("supermarket_sales.csv")

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Dashboard title
st.title("🛒 Supermarket Sales Dashboard")
st.write("Customer Purchase Analytics")

st.divider()

# 2. SIDEBAR FILTERS

st.sidebar.title("Dashboard Filters")

# Branch filter
branches = st.sidebar.multiselect(
    "Select Branch",
    df['Branch'].dropna().unique(),
    default=list(df['Branch'].dropna().unique())
)

# Product line filter
products = st.sidebar.multiselect(
    "Select Product Line",
    df['Product line'].dropna().unique(),
    default=list(df['Product line'].dropna().unique())
)

# Payment filter
payments = st.sidebar.multiselect(
    "Select Payment Method",
    df['Payment'].dropna().unique(),
    default=list(df['Payment'].dropna().unique())
)

# Customer type filter
customers = st.sidebar.multiselect(
    "Select Customer Type",
    df['Customer type'].dropna().unique(),
    default=list(df['Customer type'].dropna().unique())
)

# Apply filters
filtered_df = df[
    (df['Branch'].isin(branches)) &
    (df['Product line'].isin(products)) &
    (df['Payment'].isin(payments)) &
    (df['Customer type'].isin(customers))
]

# 3. KEY PERFORMANCE INDICATORS

st.subheader("📊 Dashboard Overview")

if not filtered_df.empty:

    total_records = len(filtered_df)
    total_sales = filtered_df['Total'].sum()
    average_sales = filtered_df['Total'].mean()
    total_quantity = filtered_df['Quantity'].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Transactions",
        total_records
    )

    col2.metric(
        "Total Sales",
        f"{total_sales:,.2f}"
    )

    col3.metric(
        "Average Sales",
        f"{average_sales:,.2f}"
    )

    col4.metric(
        "Total Quantity",
        total_quantity
    )

else:
    st.warning("No records found for the selected filters.")

st.divider()

# 4. DATASET EXPLORATION

st.subheader("📋 Dataset Information")

with st.container():

    st.write("Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    with st.expander("View Dataset Summary"):

        st.write("Dataset Shape:", filtered_df.shape)

        st.write("Data Types:")
        st.write(filtered_df.dtypes)

        st.write("Descriptive Statistics:")
        st.write(filtered_df.describe())

st.divider()

# 5. CATEGORY-WISE ANALYSIS

st.subheader("📈 Category-wise Analysis")

if not filtered_df.empty:

    col1, col2 = st.columns(2)

    # Branch-wise sales
    with col1:

        st.write("Sales by Branch")

        branch_sales = filtered_df.groupby('Branch')['Total'].sum()

        st.bar_chart(
            branch_sales,
            color="#FF8C42"
        )

    # Product-wise transaction count
    with col2:

        st.write("Product-wise Transaction Count")

        product_count = filtered_df.groupby('Product line').size()

        st.bar_chart(
            product_count,
            color="#7B61FF"
        )

st.divider()

# 6. DATA VISUALIZATIONS

st.subheader("📊 Data Visualizations")

tab1, tab2, tab3 = st.tabs([
    "🟠 Bar Chart",
    "🟢 Line Chart",
    "🟣 Scatter Plot"
])

# BAR CHART
with tab1:

    st.write("Product-wise Total Sales")

    if not filtered_df.empty:

        bar_data = filtered_df.groupby('Product line')['Total'].sum()

        st.bar_chart(
            bar_data,
            color="#FF6B6B"
        )

        st.info(
            "This chart compares total sales across different product categories."
        )

    else:
        st.warning("No data available.")

# LINE CHART
with tab2:

    st.write("Month-wise Sales Trend")

    monthly_data = filtered_df.dropna(subset=['Date']).copy()

    if not monthly_data.empty:

        monthly_data['Month'] = (
            monthly_data['Date'].dt.to_period('M').astype(str)
        )

        line_data = monthly_data.groupby('Month')['Total'].sum()

        st.line_chart(
            line_data,
            color="#20B2AA"
        )

        st.info(
            "This chart shows changes in supermarket sales over time."
        )

    else:
        st.warning("No date information available.")

# SCATTER PLOT
with tab3:

    st.write("Quantity vs Total Sales")

    if not filtered_df.empty:

        st.scatter_chart(
            filtered_df,
            x='Quantity',
            y='Total',
            color="#9B59B6"
        )

        st.info(
            "This chart shows the relationship between quantity purchased and total sales."
        )

    else:
        st.warning("No data available.")

st.divider()

# 7. SALES INSIGHTS

st.subheader("💡 Sales Insights")

if not filtered_df.empty:

    # Highest selling product
    best_product = (
        filtered_df.groupby('Product line')['Total'].sum().idxmax()
    )

    # Best performing branch
    best_branch = (
        filtered_df.groupby('Branch')['Total'].sum().idxmax()
    )

    # Most popular payment method
    popular_payment = (
        filtered_df['Payment'].value_counts().idxmax()
    )

    col1, col2, col3 = st.columns(3)

    col1.success(
        f"🏆 Highest Sales Category\n\n{best_product}"
    )

    col2.info(
        f"🏬 Best Performing Branch\n\n{best_branch}"
    )

    col3.warning(
        f"💳 Popular Payment Method\n\n{popular_payment}"
    )

else:

    st.warning("No insights available for the selected filters.")
