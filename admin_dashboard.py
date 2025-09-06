import os
from datetime import datetime
import streamlit as st
import pandas as pd

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_excels"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="📂 Admin Dashboard", layout="wide")

st.title("📂 Admin Dashboard - Upload Excel Files")

uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Save uploaded file with timestamp prefix
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File saved: {filename}")

    # Show preview
    xls = pd.ExcelFile(file_path)
    selected_sheet = st.sidebar.radio("📑 Select a sheet", xls.sheet_names)
    df = pd.read_excel(file_path, sheet_name=selected_sheet, header=0)

    st.subheader(f"📋 Preview: {selected_sheet}")
    st.dataframe(df, use_container_width=True)
else:
    st.info("👆 Upload an Excel file to save and preview")
