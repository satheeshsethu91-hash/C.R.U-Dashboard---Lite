import streamlit as st
import pandas as pd
import os

# ==============================
# Config
# ==============================
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

ADMIN_PASSWORD = "admin123"  # 🔒 Change this for security


# ==============================
# Helper functions
# ==============================
def save_uploaded_files(uploaded_files):
    """Save multiple uploaded Excel files"""
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


def list_excel_files():
    """List all Excel files in upload directory (deduplicated)"""
    excel_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".xlsx")]
    return sorted(set(excel_files))  # remove duplicates


def load_excel(file_name):
    """Load an Excel file into a DataFrame"""
    file_path = os.path.join(UPLOAD_DIR, file_name)
    return pd.ExcelFile(file_path)


def download_file(file_name):
    """Provide a download link for an uploaded file"""
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "rb") as f:
        st.download_button(
            label=f"⬇️ Download {file_name}",
            data=f,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# ==============================
# App UI
# ==============================
st.set_page_config(page_title="CRU Dashboard Lite", layout="wide")

st.title("📊 CRU Dashboard Lite")

# Role selection
role = st.radio("Login as:", ["Client", "Admin"])

# ------------------------------
# Admin Section
# ------------------------------
if role == "Admin":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:
        st.success("✅ Logged in as Admin")

        # Upload multiple files
        uploaded_files = st.file_uploader(
            "Upload Excel files",
            type=["xlsx"],
            accept_multiple_files=True
        )
        if uploaded_files:
            save_uploaded_files(uploaded_files)
            st.success(f"Uploaded {len(uploaded_files)} files successfully!")

        # List available files
        excel_files = list_excel_files()
        if excel_files:
            selected_file = st.selectbox("Choose an Excel file", excel_files)
            st.info(f"📄 Selected: {selected_file}")

            # Preview & download
            if selected_file:
                xls = load_excel(selected_file)
                sheet_names = xls.sheet_names
                sheet = st.selectbox("Select Sheet", sheet_names)
                df = pd.read_excel(xls, sheet_name=sheet)
                st.dataframe(df.head())

                download_file(selected_file)

        else:
            st.info("📂 No files uploaded yet")

    else:
        st.error("❌ Wrong password")


# ------------------------------
# Client Section
# ------------------------------
elif role == "Client":
    st.info("👤 Client Mode: View uploaded reports only")

    excel_files = list_excel_files()
    if excel_files:
        selected_file = st.selectbox("Choose an Excel file", excel_files)
        st.info(f"📄 Selected: {selected_file}")

        if selected_file:
            xls = load_excel(selected_file)
            sheet_names = xls.sheet_names
            sheet = st.selectbox("Select Sheet", sheet_names)
            df = pd.read_excel(xls, sheet_name=sheet)
            st.dataframe(df.head())

            download_file(selected_file)
    else:
        st.info("📂 No files available. Please contact Admin.")
