import streamlit as st
import pandas as pd
from charts.time_series import expenses_vs_allowance_chart
from utils.transform import monthly_allowance, monthly_expenses

def expenses_vs_allowance(expenses_df, income_df):
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