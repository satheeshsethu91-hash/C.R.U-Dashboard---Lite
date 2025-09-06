import streamlit as st
import pandas as pd
import os

# Config
st.set_page_config(page_title="📊 Client - Excel Viewer", layout="wide")
st.title("📊 Client Dashboard - Excel Viewer")

UPLOAD_DIR = "uploaded_excels"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Get all Excel files in the folder
excel_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]
excel_files.sort(reverse=True)  # latest first

if not excel_files:
    st.warning("⚠️ No Excel files available. Please ask Admin to upload files.")
else:
    selected_file = st.selectbox("📂 Select an Excel file", excel_files)
    file_path = os.path.join(UPLOAD_DIR, selected_file)

    xls = pd.ExcelFile(file_path)

    # Sidebar sheet navigation
    st.sidebar.header("📑 Sheets")
    sheet = st.sidebar.radio("Choose a sheet", xls.sheet_names)

    df = pd.read_excel(xls, sheet_name=sheet, header=0)

    st.subheader(f"📋 Data Preview: {sheet}")

    # --- Search box ---
    search_term = st.text_input("🔍 Search")
    if search_term:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
        df = df[mask]

    # --- Filters ---
    with st.expander("⚙️ Column Filters"):
        for col in df.columns:
            unique_vals = df[col].dropna().unique().tolist()
            if len(unique_vals) < 50:  # don’t show filter if too many unique values
                selected_vals = st.multiselect(f"Filter {col}", unique_vals)
                if selected_vals:
                    df = df[df[col].isin(selected_vals)]

    st.dataframe(df, use_container_width=True)
