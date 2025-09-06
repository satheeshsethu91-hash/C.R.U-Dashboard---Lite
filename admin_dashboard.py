import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Config
st.set_page_config(page_title="📂 Admin - Excel Upload", layout="wide")
st.title("📂 Admin Dashboard - Excel Upload")

UPLOAD_DIR = "uploaded_excels"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file to folder
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File saved as {filename} in {UPLOAD_DIR}/")

    # Preview the file
    xls = pd.ExcelFile(file_path)
    st.subheader("📑 Sheets in this file:")
    for sheet_name in xls.sheet_names:
        st.write(f"📄 {sheet_name}")
        df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
        st.dataframe(df, use_container_width=True)
