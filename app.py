import streamlit as st
import pandas as pd

from data.loader import load_sheet
from utils.transform import (
    monthly_expenses,
    monthly_allowance,
    top_categories, monthly_food_expenses, food_saver, projected_vs_actual_grocery_expenses
)
from charts.time_series import expenses_vs_allowance_chart, projected_weekly_grocery_expenses
from charts.category import top_category_pie, top_category_pie_by_month

st.set_page_config(page_title="Expense Dashboard", layout="wide")

expenses_df = load_sheet("expenses")
income_df = load_sheet("income")
transfer_df = load_sheet("transfer")
savers_df = load_sheet("food_savers")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📊 Main Dashboard", "📂 Raw Data"])

if page == "📊 Main Dashboard":
    st.title("International Student Expense Dashboard")
    st.text("Hi, I'm Martina! An international student trying to manage my finances while taking up a postgraduate degree in Software Engineering at the University of Sydney. This dashboard is a personal project to track and analyze my expenses as an international student. I hope that by sharing my data and insights, I can help other students who are in a similar situation to better understand their own spending habits and find ways to save money. The data is sourced from my personal records, and I have categorized my expenses into different categories such as groceries, rent, transportation, and entertainment. I will be updating this dashboard regularly to reflect my latest expenses and insights.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expenses", f"${expenses_df['Amount'].sum():,.2f}")
    col2.metric("Total Allowance", f"${income_df['Amount'].sum():,.2f}")
    col3.metric("Transfers from HSBC to my CommBank Account", f"${transfer_df['Amount'].sum():,.2f}")

    st.divider(width="stretch")
    st.header("📈 Expenses vs Allowance")
    monthly_exp = monthly_expenses(expenses_df)
    monthly_all = monthly_allowance(income_df)

    combined = pd.concat(
        [monthly_exp, monthly_all],
        ignore_index=True
    )
    st.altair_chart(
        expenses_vs_allowance_chart(combined),
        use_container_width=True
    )
    st.write("As you can see, my expenses are generally lower than my allowance. I try to keep my expenses as low as possible by availing of discounts, cooking my own food at home, and using the food pantry.")

    st.divider(width="stretch")
    st.subheader("Expenses Deep Dive")
    col1, col2 = st.columns(2)
    with col1:
        pie_df = top_categories(expenses_df)
        st.plotly_chart(top_category_pie(pie_df), theme=None)
    with col2:
        st.plotly_chart(
            top_category_pie_by_month(expenses_df),
            use_container_width=True,
            theme=None
    )
    
    st.divider(width="stretch")
    st.header("🛒 Food Savers")
    st.text("I try as much as possible to save on expenses in my grocery. Thankfully, the uni I attend has a food pantry called the Food Hub. It's highly competative to get a slot just to get a few products. These are mostly supplementary items such as canned goods, frozen food, and ready to eat meals. The postgraduates also have their own smaller pantry. Tt's similar in products but the competition is low, so we can go to the food pantry any time as long as there are stocks available. I try to avail of that too.")
    food_df, monthly_food =monthly_food_expenses(expenses_df)
    st.dataframe(monthly_food)
    st.write("I avail of Rice, Butter, Carrots, Potatoes, and Cereal from the food pantry. I try to get those items every week. I also get other items whenever there are stocks available, but those are the main items that I get every month.")
    savers_df, added_weekly_spendings, weekly_food_expense, avg_food_expense = food_saver(expenses_df,savers_df)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Weekly Food Expense")
        # st.dataframe(weekly_food_expense)
        st.write(f"Average weekly food expense: ${avg_food_expense:,.2f}")
         
    with col2:  
        st.subheader("Retail Price of Pantry Items")
        st.dataframe(savers_df)
        st.write(f"Added weekly food expense: ${added_weekly_spendings:,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"I did not realize how much I was saving by availing of the food pantry until I did this analysis. On average, I save around ${added_weekly_spendings*4:,.2f} a month on groceries by using the food pantry. That's a significant amount for a student budget! If I didn't know the pantry existed, my weekly and monthly food expenses would look like this:")
    with col2:
        weekly_long = projected_vs_actual_grocery_expenses(expenses_df, savers_df)
        st.altair_chart(
            projected_weekly_grocery_expenses(weekly_long),
            use_container_width=True
        )

    st.divider(width="stretch")
    st.header("🏡 Rent")

    st.divider(width="stretch")
    st.header("🚗 Transportation")

        
else:
    st.title("Raw Data")
    st.dataframe(expenses_df)
    st.dataframe(income_df)
    st.dataframe(transfer_df)