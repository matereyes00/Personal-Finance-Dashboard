# charts/time_series.py
import altair as alt
import pandas as pd

def expenses_vs_allowance_chart(df: pd.DataFrame):
    return (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "month_ts:T",
                timeUnit="yearmonth",
                axis=alt.Axis(format="%b %Y"),
                title="Month"
            ),
            y=alt.Y("Amount:Q", title="Amount ($)"),
            color=alt.Color("type:N", title=""),
            tooltip=["type", "Amount"]
        )
        .properties(height=400)
    )

def projected_weekly_grocery_expenses(df: pd.DataFrame):
    return (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "week:T",
                title="Week",
                axis=alt.Axis(format="%d %b %Y")
            ),
            y=alt.Y(
                "Amount:Q",
                title="Amount ($)"
            ),
            color=alt.Color(
                "Scenario:N",
                title="",
                scale=alt.Scale(
                    domain=["Actual Spend", "Projected Spend"],
                    range=["#4C78A8", "#F58518"]  # Blue = actual, Orange = projected
                )
            ),
            tooltip=[
                alt.Tooltip("Scenario:N", title="Scenario"),
                alt.Tooltip("week:T", title="Week", format="%d %b %Y"),
                alt.Tooltip("Amount:Q", title="Amount ($)", format="$.2f"),
            ]
        )
        .properties(
            height=420,
            title="Weekly Grocery Spending: Actual vs Projected"
        )
    )
