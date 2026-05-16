import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Six Store Analytics", layout="wide")
st.title("Six Store Performance Dashboard 2025")

# Data Loading Function
@st.cache_data
def load_data():
  
    # df = pd.read_csv(r'D:\PVD\store_sales.csv')
    df = pd.read_csv('store_sales.csv')
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("Filter Dashboard")
    gender = st.sidebar.multiselect(
        "Select Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    season = st.sidebar.multiselect(
        "Select Season:",
        options=df["Season"].unique(),
        default=df["Season"].unique()
    )
    category = st.sidebar.multiselect(
        "Select Category:",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    # Apply Filters
    df_selection = df.query("Gender == @gender & Season == @season & Category == @category")

    # KPI Section
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_revenue = df_selection["Amount"].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    with col2:
        avg_rating = df_selection["ItemRating"].mean()
        st.metric("Avg Rating", f"{avg_rating:.2f} \u2605")
    with col3:
        total_customers = df_selection["CustomerID"].nunique()
        st.metric("Customers", f"{total_customers}")

    st.markdown("---")
 
    # Visualizations -> baris pertama
    left_column, right_column = st.columns(2)

    with left_column:
        # Chart: Top Selling Items 
        item_sales = df_selection.groupby("ItemPurchased")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
        fig_item = px.bar(
            item_sales.head(10), 
            x="Amount", 
            y="ItemPurchased", 
            orientation='h',
            title="<b>Top 10 Products by Sales</b>",
            color_discrete_sequence=["#0083B8"] * len(item_sales),
            template="plotly_white"
        )
        fig_item.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_item, use_container_width=True)


    with right_column:
        age_bins = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 76]
        age_labels = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-75"]

    
        df_selection["Age_Group"] = pd.cut(
            df_selection["Age"], bins=age_bins, labels=age_labels, right=False
        )

        age_counts = df_selection["Age_Group"].value_counts().sort_index().reset_index()
        age_counts.columns = ["Age_Group", "count"]

    
        fig_age = px.histogram(
            age_counts, 
            x="Age_Group", 
            y="count", 
            title="<b>Customer Age Distribution</b>",
            color_discrete_sequence=["#FF6F00"],
            template="plotly_white"
        )
        
        fig_age.update_layout(
            bargap=0.01,
            xaxis_title="Age",
            yaxis_title="count"
        )
        st.plotly_chart(fig_age, use_container_width=True)


    # Visualizations -> baris ke 2
    st.markdown("---")
    
    col_bottom1, col_bottom2 = st.columns(2)

    with col_bottom1:
        # Season Performance (Line Chart)
        season_perf = df_selection.groupby("Season")["Amount"].sum().reset_index()

        fig_season = px.line(
            season_perf,
            x="Season",
            y="Amount",
            title="<b>Season Performance Trend</b>",
            markers=True,  # biar ada titik di tiap season
            template="plotly_white"
        )

        st.plotly_chart(fig_season, use_container_width=True)

    with col_bottom2:
        # Revenue by Payment Method (Pie Chart)
        gender_rev = df_selection.groupby("Gender")["Amount"].sum().reset_index()
        fig_gender = px.pie(
            gender_rev,
            values="Amount",
            names="Gender",
            title="<b>Customer Gender Revenue Percentage</b>",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    # Visualizations -> baris ke 3 
    st.markdown("---")
    col_rating1, col_rating2 = st.columns(2)

    # Menghitung rata-rata rating per produk
    avg_item_rating = df_selection.groupby("ItemPurchased")["ItemRating"].mean().reset_index()

    with col_rating1:
        # Top 10 Highest Rating
        highest_rating = avg_item_rating.sort_values("ItemRating", ascending=False).head(10)
        fig_high_rating = px.bar(
            highest_rating,
            x="ItemRating",
            y="ItemPurchased",
            orientation='h',
            title="<b>Top 10 Products by Highest Rating</b>",
            color="ItemRating",
            color_continuous_scale=["#FFFF00", "#41AB5D","#005A32"],
            template="plotly_white"
        )

        fig_high_rating.update_yaxes(autorange="reversed")
        fig_high_rating.update_xaxes(range=[3, 4],tickmode="linear",
            tick0=3.0,
            dtick=0.1)
        st.plotly_chart(fig_high_rating, use_container_width=True)


    with col_rating2:
        # Top 10 Lowest Rating
        lowest_rating = avg_item_rating.sort_values("ItemRating", ascending=True).head(10)
        fig_low_rating = px.bar(
            lowest_rating,
            x="ItemRating",
            y="ItemPurchased",
            orientation='h',
            title="<b>Top 10 Products by Lowest Rating</b>",
            color="ItemRating",
            color_continuous_scale=["#800000", "#E44444", "#FF8C00"],
            template="plotly_white"
        )
        fig_low_rating.update_xaxes(range=[3, 4],tickmode="linear",
            tick0=3.0,
            dtick=0.1)
        st.plotly_chart(fig_low_rating, use_container_width=True)

    # Sales Distribution by Category 
    st.markdown("---")
    # Visualizations -> baris ke 4 
    cat_dist = df_selection.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
    fig_cat = px.bar(
        cat_dist,
        x="Category",
        y="Amount",
        title="<b>Sales Distribution by Category</b>",
        color="Category",
        template="plotly_white"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # Data Table 
    st.write("### Filtered Raw Data")
    st.dataframe(df_selection)

except Exception as e:
    st.error(f"An error occurred: {e}")