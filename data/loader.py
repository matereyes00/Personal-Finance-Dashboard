# data/loader.py
import os
from pathlib import Path

import pandas as pd
import gspread
import streamlit as st
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")
if not SHEET_ID:
    raise RuntimeError("SHEET_ID is not set")


def get_credentials() -> Credentials:
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # ✅ TRY STREAMLIT CLOUD FIRST (SAFE)
    try:
        creds_dict = st.secrets["gcp_service_account"]
        return Credentials.from_service_account_info(
            creds_dict,
            scopes=scopes
        )
    except StreamlitSecretNotFoundError:
        pass
    except KeyError:
        pass

    # ✅ FALL BACK TO LOCAL DEVELOPMENT
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS is not set for local development"
        )

    base_dir = Path(__file__).resolve().parents[1]
    credentials_file = base_dir / credentials_path

    if not credentials_file.exists():
        raise RuntimeError(
            f"Service account file not found: {credentials_file}"
        )

    return Credentials.from_service_account_file(
        credentials_file,
        scopes=scopes
    )


@st.cache_data(ttl=300)
def load_sheet(sheet_name: str) -> pd.DataFrame:
    creds = get_credentials()
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID) # type: ignore
    worksheet = sheet.worksheet(sheet_name)

    data = worksheet.get_all_records()
    return pd.DataFrame(data)
