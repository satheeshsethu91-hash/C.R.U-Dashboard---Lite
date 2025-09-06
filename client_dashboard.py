import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Client Dashboard", layout="wide")
st.title("📊 Client Dashboard - Excel Viewer")

DATA_FOLDER = "data"

@st.cache_data
def load_excel(file_path):
    # Do not alter headers, even if merged
    xls = pd.ExcelFile(file_path)
    sheets = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)  # keep raw headers
        sheets[sheet_name] = df
    return sheets

# --- Get available Excel files ---
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".xlsx")]

if files:
    # Sort files by modified time (latest first)
    files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(DATA_FOLDER, x)), reverse=True)

    # Dropdown to choose file
    selected_file = st.sidebar.selectbox("📂 Select Excel File", files)
    file_path = os.path.join(DATA_FOLDER, selected_file)

    # Load selected Excel
    sheets = load_excel(file_path)

    # Sidebar navigation for sheets
    st.sidebar.header("📑 Sheets")
    selected_sheet = st.sidebar.radio("Select a sheet", list(sheets.keys()))

    df = sheets[selected_sheet]

    st.subheader(f"📋 Data Preview: {selected_sheet} (from {selected_file})")

    # --- Search ---
    search_term = st.text_input("🔍 Search text")
    filtered_df = df
    if search_term:
        mask = df.astype(str).apply(lambda row: row.str.contains(search_term, case=False, na=False).any(), axis=1)
        filtered_df = df[mask]

    # --- Column filters ---
    with st.expander("⚙️ Column Filters"):
        for col in filtered_df.columns:
            options = st.multiselect(f"Filter column {col}", filtered_df[col].dropna().unique())
            if options:
                filtered_df = filtered_df[filtered_df[col].isin(options)]

    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("⚠️ No Excel files available. Please ask Admin to upload files.")
