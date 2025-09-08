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

# ----------------- HELPER: GET UNIQUE FILES -----------------
def get_unique_files():
    excel_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]
    # Sort by timestamp in filename (newest first)
    excel_files.sort(reverse=True)

    # Deduplicate by original filename (after timestamp)
    unique_files = {}
    for f in excel_files:
        original_name = "_".join(f.split("_")[1:])  # remove timestamp
        if original_name not in unique_files:
            unique_files[original_name] = f
    return list(unique_files.values())

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
        # Save file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffe_
