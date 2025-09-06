import os
import pandas as pd
import streamlit as st

UPLOAD_DIR = "uploaded_excels"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="📊 Client Dashboard", layout="wide")

st.title("📊 Client Dashboard - Excel Viewer")

excel_files = sorted(os.listdir(UPLOAD_DIR), reverse=True)

if excel_files:
    selected_file = st.selectbox("📂 Choose an Excel file", excel_files)
    file_path = os.path.join(UPLOAD_DIR, selected_file)

    xls = pd.ExcelFile(file_path)
    selected_sheet = st.sidebar.radio("📑 Select a sheet", xls.sheet_names)

    df = pd.read_excel(file_path, sheet_name=selected_sheet, header=0)

    st.subheader(f"📋 Data Preview: {selected_sheet}")

    # --- Search ---
    search_term = st.text_input("🔍 Search")
    if search_term:
        mask = df.apply(
            lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(),
            axis=1
        )
        df = df[mask]

    # --- Column Filters ---
    with st.expander("⚙️ Column Filters"):
        for col in df.columns:
            if df[col].dtype == "object":
                options = st.multiselect(f"Filter {col}", df[col].dropna().unique())
                if options:
                    df = df[df[col].isin(options)]

    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ No Excel files available. Please ask Admin to upload files.")
