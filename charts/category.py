
import plotly.express as px
import pandas as pd
import streamlit as st

def top_category_pie(df: pd.DataFrame):
    fig = px.pie(
        df,
        values="Amount",
        names="Category",
        title="Top Expense Categories"
    )
    return fig

def top_category_pie_by_month(expenses_df: pd.DataFrame):
    df = expenses_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")
    df["month_label"] = df["month"].dt.to_timestamp().dt.strftime("%b %Y")

    selected_month = st.selectbox(
        "Select Month",
        options=sorted(df["month_label"].unique())
    )

    monthly_df = df[df["month_label"] == selected_month]

    category_df = (
        monthly_df
        .groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

    top5 = category_df.head(5)
    others_sum = category_df.iloc[5:]["Amount"].sum()

    if others_sum > 0:
        top5 = pd.concat([
            top5,
            pd.DataFrame({"Category": ["Other"], "Amount": [others_sum]})
        ])

    fig = px.pie(
        top5,
        values="Amount",
        names="Category",
        title=f"Expense Breakdown – {selected_month}",
        hole=0.4
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Amount: $%{value:,.2f}<br>"
            "Percentage: %{percent}"
        )
    )

    return fig
