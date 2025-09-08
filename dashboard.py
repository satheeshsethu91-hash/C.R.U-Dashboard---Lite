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
        # Save file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save the uploaded file (keep older ones too)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ File saved as {filename}")

    # ----------------- FILE MANAGEMENT -----------------
    st.subheader("🗑️ File Management")

    excel_files = list(set([f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]))
    excel_files.sort(reverse=True)

    if excel_files:
        # Dropdown for selecting file to view
        selected_file = st.selectbox("📂 Select Excel File", excel_files)
        file_path = os.path.join(UPLOAD_DIR, selected_file)

        # Delete all
        if st.button("❌ Delete All Uploaded Files"):
            for f in excel_files:
                os.remove(os.path.join(UPLOAD_DIR, f))
            st.success("✅ All uploaded files deleted.")
            st.stop()

        # Delete single file
        file_to_delete = st.selectbox("🗑️ Select a file to delete", excel_files, key="delete_file")
        if st.button("🗑️ Delete Selected File"):
            os.remove(os.path.join(UPLOAD_DIR, file_to_delete))
            st.success(f"✅ File '{file_to_delete}' deleted.")
            st.stop()

        # Display sheets
        xls = pd.ExcelFile(file_path)
        st.sidebar.header("📑 Sheets")
        sheet = st.sidebar.radio("Choose a sheet", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=sheet, header=0)

        st.subheader(f"📋 Data Preview: {sheet}")

        # Download Option
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
        st.info("📂 No files uploaded
