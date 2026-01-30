import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Silver Dashboard", layout="wide")

st.markdown(
    """
    <style>
        .main {
            background-color: #f4f7f9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

section = st.sidebar.radio("Navigation", ["Price Calculator", "Historical Prices", "State-wise Purchases", "Silver Insights"])

hist = pd.read_csv("historical_silver_price.csv")
state_data = pd.read_csv("state_wise_silver_purchased_kg.csv")
hist.columns = ["Year", "Month", "Silver_Price_INR_per_kg"]

PRIMARY = "#006d77"
SECONDARY = "#83c5be"
ACCENT = "#edf6f9"

plt.rcParams.update({
    "axes.facecolor": "white",
    "figure.facecolor": ACCENT,
    "axes.edgecolor": PRIMARY,
    "axes.labelcolor": PRIMARY,
    "xtick.color": PRIMARY,
    "ytick.color": PRIMARY,
    "text.color": PRIMARY,
    "axes.titleweight": "bold",
    "axes.titlecolor": PRIMARY,
    "axes.grid": True,
    "grid.color": SECONDARY,
    "grid.linestyle": "--",
    "grid.alpha": 0.4
})

if section == "Price Calculator":
    st.header("Silver Price Calculator")

    col1, col2, col3 = st.columns(3)

    with col1:
        weight = st.number_input("Enter weight", min_value=0.0, value=10.0)

    with col2:
        unit = st.selectbox("Unit", ["grams", "kilograms"])

    with col3:
        price_per_gram = st.number_input("Current silver price per gram (INR)", min_value=1.0, value=75.0)

    if unit == "kilograms":
        weight_in_grams = weight * 1000
    else:
        weight_in_grams = weight

    total_cost_inr = weight_in_grams * price_per_gram
    st.write(f"Total Cost: ₹ {total_cost_inr:,.2f}")

    rate = 0.012
    total_cost_usd = total_cost_inr * rate
    st.write(f"USD Equivalent: $ {total_cost_usd:,.2f}")


elif section == "Historical Prices":
    st.header("Historical Silver Price Chart")

    price_filter = st.radio(
        "Filter based on price per kg:",
        ["≤ 20000", "20000 – 30000", "≥ 30000"]
    )

    if price_filter == "≤ 20000":
        df_filtered = hist[hist["Silver_Price_INR_per_kg"] <= 20000]
    elif price_filter == "20000 – 30000":
        df_filtered = hist[
            (hist["Silver_Price_INR_per_kg"] >= 20000) &
            (hist["Silver_Price_INR_per_kg"] <= 30000)
        ]
    else:
        df_filtered = hist[hist["Silver_Price_INR_per_kg"] >= 30000]

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    for y in df_filtered["Year"].unique():
        df_year = df_filtered[df_filtered["Year"] == y]
        ax1.plot(df_year["Month"], df_year["Silver_Price_INR_per_kg"], marker="o", linewidth=2.2, color=PRIMARY)

    ax1.set_title("Historical Silver Prices (Filtered)")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Price (INR per kg)")
    st.pyplot(fig1)


elif section == "State-wise Purchases":
    st.header("State-wise Silver Purchases")

    state_data_sorted = state_data.sort_values("Silver_Purchased_kg", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.bar(state_data_sorted["State"], state_data_sorted["Silver_Purchased_kg"], color=SECONDARY, edgecolor=PRIMARY, linewidth=1.2)
    ax2.set_xticklabels(state_data_sorted["State"], rotation=45, ha="right")
    ax2.set_title("State-wise Silver Purchases")
    ax2.set_xlabel("State")
    ax2.set_ylabel("Silver Purchased (kg)")
    st.pyplot(fig2)


elif section == "Silver Insights":
    st.header("Silver Sales Insights")

    top5 = state_data.sort_values("Silver_Purchased_kg", ascending=False).head(5)

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.bar(top5["State"], top5["Silver_Purchased_kg"], color=PRIMARY, edgecolor=PRIMARY)
    ax3.set_title("Top 5 States with Highest Silver Purchases")
    ax3.set_ylabel("Silver Purchased (kg)")
    st.pyplot(fig3)

    st.subheader("January Month Silver Sales")

    jan_df = pd.DataFrame({
        "State": state_data["State"],
        "January_Sales_kg": state_data["Silver_Purchased_kg"] / 12
    })

    fig4, ax4 = plt.subplots(figsize=(12, 4))
    ax4.plot(jan_df["State"], jan_df["January_Sales_kg"], marker="o", linewidth=2.2, color=PRIMARY)
    ax4.set_title("January Silver Sales Across States")
    ax4.set_xticklabels(jan_df["State"], rotation=45, ha="right")
    ax4.set_ylabel("January Sales (kg)")
    st.pyplot(fig4)

    st.dataframe(jan_df)
