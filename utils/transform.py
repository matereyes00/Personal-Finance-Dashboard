# utils/transform.py
import streamlit as st
import pandas as pd

def monthly_expenses(expenses_df: pd.DataFrame) -> pd.DataFrame:
    df = expenses_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("month")["Amount"]
        .sum()
        .reset_index()
    )

    monthly["month_ts"] = monthly["month"].dt.to_timestamp()
    monthly["type"] = "Expenses"
    return monthly


def monthly_allowance(income_df: pd.DataFrame) -> pd.DataFrame:
    df = income_df.copy()
    df["Category"] = df["Category"].str.strip()

    allowance_df = df[df["Category"] == "Allowance"].copy()
    allowance_df["date"] = pd.to_datetime(allowance_df["date"])
    allowance_df["month"] = allowance_df["date"].dt.to_period("M")

    monthly = (
        allowance_df.groupby("month")["Amount"]
        .sum()
        .reset_index()
    )

    monthly["month_ts"] = monthly["month"].dt.to_timestamp()
    monthly["type"] = "Allowance"
    return monthly


def top_categories(expenses_df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    df = (
        expenses_df
        .groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    ) # type: ignore

    top_n = df.head(n)
    others_sum = df.iloc[n:]["Amount"].sum()

    if others_sum > 0:
        other = pd.DataFrame({
            "Category": ["Other"],
            "Amount": [others_sum]
        })
        top_n = pd.concat([top_n, other], ignore_index=True)

    return top_n


def top_categories_by_month(expenses_df: pd.DataFrame, month: str, n: int = 5) -> pd.DataFrame:
    df = expenses_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    month_df = df[df["month"] == month]

    top_n = df.head(n)
    others_sum = df.iloc[n:]["Amount"].sum()

    if others_sum > 0:
        other = pd.DataFrame({
            "Category": ["Other"],
            "Amount": [others_sum]
        })
        top_n = pd.concat([top_n, other], ignore_index=True)

    return top_n

    # return top_categories(month_df, n)


def monthly_food_expenses(expenses_df: pd.DataFrame):
    df = expenses_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    food_df = df[df["Category"] == "Grocery"].copy()
    monthly_food = (
        food_df.groupby("month")["Amount"]
        .sum()
        .reset_index()
    )

    return food_df, monthly_food


def food_saver(expenses_df: pd.DataFrame, savers_df: pd.DataFrame):
    expenses = expenses_df.copy()
    savers = savers_df.copy()
    expenses["date"] = pd.to_datetime(expenses["date"])
    expenses["week"] = expenses["date"].dt.to_period("W")

    expenses_weekly = expenses[expenses["Category"] == "Grocery"].copy()
    expenses_weekly["week"] = expenses_weekly["week"].dt.to_timestamp(how="start")
    
    added_weekly_spendings = savers["Retail Price"].sum()


    avg_food_expense = expenses_weekly["Amount"].mean()
    # st.write(f"Average weekly food expense: ${avg_food_expense:,.2f}")

    weekly_food_expenses = (
        expenses_weekly.groupby("week")["Amount"]
        .sum()
        .reset_index()
    )

    return savers, added_weekly_spendings, weekly_food_expenses, avg_food_expense


def projected_vs_actual_grocery_expenses(expenses_df: pd.DataFrame, savers_df: pd.DataFrame):
    expenses = expenses_df.copy()
    savers = savers_df.copy()
    added_weekly_spendings = savers["Retail Price"].sum()

    expenses["date"] = pd.to_datetime(expenses["date"])
    expenses["week"] = expenses["date"].dt.to_period("W")
    '''
    Multiverse where pantry did not exist and I had to buy the items at retail price. This is a very rough estimate since it does not take into account the variability of the prices of the items that I get from the pantry, but it gives a general idea of how much I would have spent on groceries if I did not avail of the food pantry.
    '''
    weekly_food_expense = expenses[expenses["Category"] == "Grocery"].copy()
    weekly_food_expense["week"] = weekly_food_expense["week"].dt.to_timestamp(how="start")

    weekly_food_expense["Actual Spend"] = weekly_food_expense["Amount"]
    weekly_food_expense["Projected Spend"] = (
        weekly_food_expense["Amount"] + added_weekly_spendings
    )

    # ✅ DROP original Amount BEFORE melt
    weekly_food_expense = weekly_food_expense.drop(columns=["Amount"])

    weekly_long = weekly_food_expense.melt(
        id_vars="week",
        value_vars=["Actual Spend", "Projected Spend"],
        var_name="Scenario",
        value_name="Amount"
    )


    weekly_long_agg = (
        weekly_long
        .groupby(["week", "Scenario"], as_index=False)["Amount"]
        .sum()
    )

    return weekly_long_agg