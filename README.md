# 🧾 International Student Expense Dashboard

A Streamlit dashboard for tracking, analyzing, and visualizing personal expenses as an international student. The app connects directly to Google Sheets using a Google Cloud **service account**, allowing you to update expenses without managing CSV files.

---

## ✨ Features

- 📊 Weekly and monthly expense analysis
- 🛒 Grocery spending (actual vs projected without pantry access)
- 🥧 Interactive category breakdowns (top 5 + “Other”)
- 📈 Time-series charts built with Altair
- 🔐 Secure Google Sheets integration
- 🧠 Clean separation of data loading, transforms, and charts

---

## 🗂 Project Structure

```
student-expenses-dashboard/
│
├── app.py
├── requirements.txt
├── .env
│
├── data/
│   └── loader.py
├── utils/
│   └── transform.py
├── charts/
│   ├── time_series.py
│   └── category.py
├── creds/
│   └── service_account.json
└── README.md
```

---

## ✅ Prerequisites

- Python **3.10+** (3.11 recommended)
- Google account
- Google Sheet for expenses

---

## 🧹 1. Google Sheets Setup

Create a Google Sheet with these tabs:

### `expenses`

| date | Category | Amount |
|------|----------|--------|
| 2026-02-16 | Grocery | 25.57 |
| 2026-02-18 | Transport | 4.20 |

### `income` (optional)

| date | Category | Amount |
|------|----------|--------|
| 2026-02-01 | Allowance | 1200 |

### `savers`

| Item | Retail Price |
|------|-------------|
| Rice | 12.50 |

> Column names are case-sensitive and must match exactly.

---

## ☁️ 2. Google Cloud Console Setup

### Create Project
- Go to https://console.cloud.google.com/
- Create a new project

### Enable Google Sheets API
- APIs & Services → Library → Enable **Google Sheets API**

### Create Service Account
- IAM & Admin → Service Accounts → Create
- Name: `streamlit-sheets-reader`
- Skip role assignment

### Create JSON Key
- Open service account → Keys → Add Key → JSON
- Download and place it at:

```
creds/service_account.json
```

### Share Google Sheet
Share your Google Sheet with the service account email as **Viewer**.

---

## 🔐 3. Environment Variables

Create a `.env` file:

```env
GOOGLE_APPLICATION_CREDENTIALS=creds/service_account.json
SHEET_ID=your_google_sheet_id_here
```

The `SHEET_ID` is found in the Google Sheets URL:

```
https://docs.google.com/spreadsheets/d/THIS_PART/edit
```

---

## 🐍 4. Python Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Example `requirements.txt`

```text
streamlit
pandas
gspread
google-auth
python-dotenv
altair
plotly
```

---

## ▶️ 5. Run the App

```bash
streamlit run app.py
```

Open: http://localhost:8501

---

## 🧠 Pantry Savings Logic

- **Actual Spend**: Weekly grocery sum
- **Projected Spend**: Actual + total retail price of pantry items
- The gap between lines shows **weekly savings**

---

## 🛑 Common Issues

- Sheet not shared with service account
- Using `Period` without `.dt.to_timestamp(how="start")`
- Missing `.env` variables

---

## 📜 License

Personal / educational use only.
