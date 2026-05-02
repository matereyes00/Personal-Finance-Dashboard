import streamlit as st
import pandas as pd

from utils.conversion_rate import get_rates
STREAMING_SERVICES = {
    # "Netflix": 9.99,
    "Disney+": 15.99,
    # "Apple TV+": 15.99,
    # "YouTube Premium": 16.99,
}

def entertainment_cut(expenses_df):

    st.header("📺 Streaming Services – Expense Cut Simulator")
    # Work on a clean copy
    expenses = expenses_df.copy()
    expenses["date"] = pd.to_datetime(expenses["date"])
    expenses["month"] = expenses["date"].dt.to_period("M")

    # ✅ Use the same DataFrame everywhere
    total_expenses = expenses["Amount"].sum()

    disney_df = expenses[
        expenses["Item"].str.contains("Disney", case=False, na=False)
    ]

    disney_total = disney_df["Amount"].sum()

    monthly_disney = (
        disney_df
        .groupby("month")["Amount"]
        .sum()
        .reset_index()
    )

    avg_monthly_savings = monthly_disney["Amount"].mean()
    yearly_savings = avg_monthly_savings * 12

    rates = get_rates("AUD")
    php_rate = rates["PHP"]
    total_expenses_php = total_expenses * php_rate
    expenses_without_disney = total_expenses - disney_total
    expenses_without_disney_php = expenses_without_disney * php_rate
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total expenses (actual)",
        f"${total_expenses:,.2f}"
    )
    col1.caption(f"Current AUD → PHP rate: ₱{total_expenses_php:,.2f}")

    col2.metric(
        "Total spent on Disney+",
        f"${disney_total:,.2f}"
    )

    col3.metric(
        "Total expenses without Disney+",
        f"${expenses_without_disney:,.2f}"
    )
    col3.caption(f"Current AUD → PHP rate: ₱{expenses_without_disney_php:,.2f}")

    st.success(
        f"If I had cancelled Disney+, my total expenses would be "
        f"**${disney_total:,.2f} lower**."
    )