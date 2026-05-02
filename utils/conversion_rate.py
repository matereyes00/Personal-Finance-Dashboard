import streamlit as st
import requests


@st.cache_data(ttl=3600)  # cache for 1 hour
def get_rates(base_currency: str) -> dict:
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["rates"]
