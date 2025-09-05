import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path
from convert import convert_excel_to_glossary

st.set_page_config(page_title="Excel → CSV Converter (Multi-files)", layout="centered")
st.title("📑 Excel Glossary → CSV Converter (Multi-files)")
st.write("Upload nhiều file Excel glossary và tải về file CSV chuẩn cho OpenMetadata.")

# Cho phép upload nhiều file
uploaded_files = st.file_uploader(
    "Chọn nhiều file Excel",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Đã tải lên {len(uploaded_files)} file")

    if st.button("Convert tất cả"):
        for uploaded_file in uploaded_files:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = Path(tmpdir) / uploaded_file.name
                out_csv = Path(tmpdir) / (src.stem + "_converted.csv")

                # Lưu file Excel tạm
                with open(src, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Convert sang CSV bằng code convert.py
                convert_excel_to_glossary(src, out_csv)

                # Hiển thị preview
                df_preview = pd.read_csv(out_csv)
                st.subheader(f"📊 Preview kết quả cho {uploaded_file.name}")
                st.dataframe(df_preview.head())

                # Cho tải về file CSV
                with open(out_csv, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Tải CSV cho {uploaded_file.name}",
                        data=f,
                        file_name=out_csv.name,
                        mime="text/csv"
                    )
