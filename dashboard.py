import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Excel Dashboard", layout="wide")
UPLOAD_DIR = "uploaded_excels"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ----------------- ROLE SELECTION -----------------
st.sidebar.title("🔑 Role Selection")
role = st.sidebar.radio("Select Role", ["Client", "Admin"])

# ----------------- ADMIN MODE -----------------
if role == "Admin":
    st.title("📂 Admin Dashboard")

    # Simple password gate
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password != "admin123":
        st.warning("Please enter the correct Admin password to continue.")
        st.stop()

    # File uploader
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    if uploaded_file:
        # Save file with timestamp to avoid duplicates
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ File saved as {filename}")

    # List available files
    excel_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]
    excel_files.sort(reverse=True)

    if excel_files:
        selected_file = st.selectbox("📂 Select a file to view", excel_files)
        file_path = os.path.join(UPLOAD_DIR, selected_file)
        xls = pd.ExcelFile(file_path)

        # Sidebar navigation
        st.sidebar.header("📑 Sheets")
        sheet = st.sidebar.radio("Choose a sheet", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet, header=0)

        st.subheader(f"📋 Data Preview: {sheet}")

        # Search
        search_term = st.text_input("🔍 Search")
        if search_term:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            df = df[mask]

        # Filters
        with st.expander("⚙️ Column Filters"):
            for col in df.columns:
                unique_vals = df[col].dropna().unique().tolist()
                if len(unique_vals) < 50:
                    selected_vals = st.multiselect(f"Filter {col}", unique_vals)
                    if selected_vals:
                        df = df[df[col].isin(selected_vals)]

        st.dataframe(df, use_container_width=True)

    else:
        st.info("📂 No files uploaded yet.")

# ----------------- CLIENT MODE -----------------
else:
    st.title("📊 Client Dashboard")

    excel_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]
    excel_files.sort(reverse=True)

    if not excel_files:
        st.warning("⚠️ No Excel files available. Please ask Admin to upload.")
    else:
        selected_file = st.selectbox("📂 Select a file", excel_files)
        file_path = os.path.join(UPLOAD_DIR, selected_file)
        xls = pd.ExcelFile(file_path)

        # Sidebar navigation
        st.sidebar.header("📑 Sheets")
        sheet = st.sidebar.radio("Choose a sheet", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet, header=0)

        st.subheader(f"📋 Data Preview: {sheet}")

        # Search
        search_term = st.text_input("🔍 Search")
        if search_term:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
            df = df[mask]

        # Filters
        with st.expander("⚙️ Column Filters"):
            for col in df.columns:
                unique_vals = df[col].dropna().unique().tolist()
                if len(unique_vals) < 50:
                    selected_vals = st.multiselect(f"Filter {col}", unique_vals)
                    if selected_vals:
                        df = df[df[col].isin(selected_vals)]

        st.dataframe(df, use_container_width=True)
