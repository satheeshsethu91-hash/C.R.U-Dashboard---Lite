import streamlit as st
import os
from datetime import datetime

# Directory for storing uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("📊 Excel Dashboard - Admin Upload")

# File uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = uploaded_file.name.split(".")[0]   # e.g., Report
    ext = uploaded_file.name.split(".")[-1]        # e.g., xlsx
    filename = f"{base_name}_{timestamp}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save new upload
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 🔥 Remove older versions of the same file
    for old_file in os.listdir(UPLOAD_DIR):
        if old_file.startswith(base_name + "_") and old_file != filename:
            os.remove(os.path.join(UPLOAD_DIR, old_file))

    st.success(f"✅ Latest version saved as {filename}. Older versions removed.")

# Dropdown to select available files
uploaded_files = sorted(os.listdir(UPLOAD_DIR), reverse=True)

if uploaded_files:
    selected_file = st.selectbox("📂 Choose a file to view:", uploaded_files)
    st.info(f"You selected: **{selected_file}**")
else:
    st.warning("⚠️ No files uploaded yet.")
