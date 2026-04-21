# data/loader.py
import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not CREDENTIALS_PATH:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS is not set")

BASE_DIR = Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = BASE_DIR / CREDENTIALS_PATH


@st.cache_data(ttl=300)
def load_sheet(sheet_name: str) -> pd.DataFrame:
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=scopes
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID) # type: ignore
    worksheet = sheet.worksheet(sheet_name)

    data = worksheet.get_all_records()
    return pd.DataFrame(data)