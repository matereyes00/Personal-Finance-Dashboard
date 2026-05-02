import streamlit as st
from charts.time_series import projected_weekly_grocery_expenses
from data.loader import load_sheet
from utils.transform import food_saver, monthly_food_expenses, projected_vs_actual_grocery_expenses

expenses_df = load_sheet("expenses")
income_df = load_sheet("income")
transfer_df = load_sheet("transfer")
savers_df = load_sheet("food_savers")


def food_savers(expenses_df, savers_df, monthly_food_expenses, food_saver, projected_vs_actual_grocery_expenses):
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