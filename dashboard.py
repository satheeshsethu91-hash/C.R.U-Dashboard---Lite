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

# ----------------- HELPER FUNCTION -----------------
def get_excel_files():
    """Return list of unique uploaded Excel files (sorted by latest first)."""
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]
    # Remove duplicates by filename (keep latest timestamped one)
    unique = {}
    for f in sorted(files, reverse=True):
        name = "_".join(f.split("_")[1:])  # remove timestamp prefix
        if name not in unique:
            unique[name] = f
    return list(unique.values())

# ----------------- ADMIN MODE -----------------
if role == "Admin":
    st.title("📂 Admin Dashboard")

    # Simple password gate
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password != "admin123":
        st.warning("Please enter the correct Admin password to continue.")
        st.stop()

    # File uploader (multiple files allowed)
    uploaded_files = st.file_uploader("Upload Excel File(s)", type=["xlsx"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save each file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uploaded_file.name}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"✅ File saved as {filename}")

    # ----------------- FILE MANAGEMENT -----------------
    st.subheader("🗂️ File Management")

    excel_files = get_excel_files()

    if excel_files:
        # Dropdown to choose a file
        selected_file = st.selectbox("📂 Select a file", excel_files)
        file_path = os.path.join(UPLOAD_DIR, selected_file)

        # Delete all files
        if st.button("❌ Delete All Files"):
            for f in os.listdir(UPLOAD_DIR):
                os.remove(os.path.join(UPLOAD_DIR, f))
            st.success("✅ All files deleted.")
            st.stop()

        # Delete selected file
        if st.button("🗑️ Delete Selected File"):
            os.remove(file_path)
            st.success(f"✅ File '{selected_file}' deleted.")
            st.stop()

        # Load Excel file
        xls = pd.ExcelFile(file_path)
        st.sidebar.header("📑 Sheets")
        sheet = st.sidebar.radio("Choose a sheet", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet, header=0)

        st.subheader(f"📋 Data Preview: {sheet}")

        # Download option
        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Excel File",
                data=f,
                file_name=selected_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Search
        search_term = st.text_input("🔍 Search")
        if search_term:
            mask = df.apply(
                lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(),
                axis=1
            )
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
    st.title("📊 Commodities Interactive Dashboard")

    excel_files = get_excel_files()

    if not excel_files:
        st.warning("⚠️ No Excel files available. Please ask Admin to upload.")
    else:
        # Dropdown to choose among uploaded files
        selected_file = st.selectbox("📂 Select Excel File", excel_files)
        file_path = os.path.join(UPLOAD_DIR, selected_file)

        # Load Excel file
        xls = pd.ExcelFile(file_path)
        st.sidebar.header("📑 Sheets")
        sheet = st.sidebar.radio("Choose a sheet", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet, header=0)

        st.subheader(f"📋 Data Preview: {sheet}")

        # Download option
        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Excel File",
                data=f,
                file_name=selected_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Search
        search_term = st.text_input("🔍 Search")
        if search_term:
            mask = df.apply(
                lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(),
                axis=1
            )
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
