import streamlit as st


def expenses_deep_dive(expenses_df, top_categories, top_category_pie, top_category_pie_by_month):
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