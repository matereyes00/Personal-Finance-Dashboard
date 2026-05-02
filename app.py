import streamlit as st
import pandas as pd
from sections.expenses_vs_allowance import expenses_vs_allowance
from sections.food_savers import food_savers
from sections.cheap_alternatives import cheap_alternatives
from sections.expenses_deep_dive import expenses_deep_dive
from data.loader import load_sheet
from utils.transform import (
    monthly_expenses,
    monthly_allowance,
    top_categories, monthly_food_expenses, food_saver, projected_vs_actual_grocery_expenses
)
from charts.time_series import expenses_vs_allowance_chart, projected_weekly_grocery_expenses
from charts.category import top_category_pie, top_category_pie_by_month
from utils.conversion_rate import get_rates

from sections.cut_expenses.rent import rent
from sections.cut_expenses.entertainment import entertainment_cut

st.set_page_config(page_title="Expense Dashboard", layout="wide")

LOGO_SIZE = 200
IMG_SIZE = 200

expenses_df = load_sheet("expenses")
income_df = load_sheet("income")
transfer_df = load_sheet("transfer")
savers_df = load_sheet("food_savers")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📊 Main Dashboard", "Cutting Expenses", "📂 Raw Data"])

if page == "📊 Main Dashboard":
    st.title("International Student Expense Dashboard")
    st.text("Hi, I'm Martina! An international student trying to manage my finances while taking up a postgraduate degree in Software Engineering at the University of Sydney. This dashboard is a personal project to track and analyze my expenses as an international student. I hope that by sharing my data and insights, I can help other students who are in a similar situation to better understand their own spending habits and find ways to save money. The data is sourced from my personal records, and I have categorized my expenses into different categories such as groceries, rent, transportation, and entertainment. I will be updating this dashboard regularly to reflect my latest expenses and insights.")

    # st.caption(
    #     "Running in Streamlit Cloud"
    #     if "gcp_service_account" in st.secrets
    #     else "Running locally"
    # )


    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expenses", f"${expenses_df['Amount'].sum():,.2f}")
    col2.metric("Total Allowance", f"${income_df['Amount'].sum():,.2f}")
    col3.metric("Transfers from HSBC to my CommBank Account", f"${transfer_df['Amount'].sum():,.2f}")

    st.divider(width="stretch")
    st.header("📈 Expenses vs Allowance")
    expenses_vs_allowance(expenses_df, income_df)

    st.divider(width="stretch")
    st.subheader("Expenses Deep Dive")
    expenses_deep_dive(expenses_df, top_categories, top_category_pie, top_category_pie_by_month)
    
    st.divider(width="stretch")
    st.header("🛒 Food Savers")
    food_savers(expenses_df, savers_df, monthly_food_expenses, food_saver, projected_vs_actual_grocery_expenses)

    st.subheader("Finding cheap alternatives")
    cheap_alternatives()

    st.divider(width="stretch")
    st.header("🏡 Rent")

    st.divider(width="stretch")
    st.header("🚗 Transportation")

elif page == "Cutting Expenses":
    st.title("Cutting Expenses")
    # st.write("Here are some of the strategies I use to cut down on my expenses:")
    # st.markdown("- **Cooking at home**: I try to cook most of my meals at home instead of eating out. This not only saves me money but also allows me to eat healthier.")
    # st.markdown("- **Using discounts and coupons**: I always look for discounts and coupons when shopping for groceries or other essentials. I also take advantage of student discounts whenever possible.")
    # st.markdown("- **Buying in bulk**: For non-perishable items, I buy in bulk to save money in the long run. This is especially helpful for items like rice, pasta, and canned goods.")
    # st.markdown("- **Using public transportation**: Instead of owning a car, I use public transportation to get around. This saves me money on gas, insurance, and maintenance.")
    # st.markdown("- **Finding free or low-cost entertainment**: I look for free or low-cost entertainment options, such as visiting parks, attending community events, or watching movies at home instead of going to the cinema.")
    rent()
    entertainment_cut(expenses_df=expenses_df)
        
else:
    st.title("Raw Data")
    st.dataframe(expenses_df)
    st.dataframe(income_df)
    st.dataframe(transfer_df)