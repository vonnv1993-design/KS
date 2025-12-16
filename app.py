import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Vietnam Airlines | IT System Survey",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# STYLE (Dark Mode – VNA)
# =========================
st.markdown("""
<style>
body {
    background-color: #0B1C2D;
    color: #F5C542;
}
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    padding: 10px;
}
.stats-card {
    background: #102A43;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.stats-number {
    font-size: 26px;
    color: #F5C542;
    font-weight: bold;
}
.stats-label {
    font-size: 13px;
    color: #E0E0E0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

form_data = st.session_state.form_data

def set_val(key, val):
    form_data[key] = val

# =========================
# PDF EXPORT
# =========================
def export_pdf(data: dict):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>VIETNAM AIRLINES – IT SYSTEM SURVEY</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    for section, title in [
        ("A", "A. Thông tin chung"),
        ("B", "B. Hạ tầng"),
        ("C", "C. Dữ liệu"),
        ("D", "D. Tích hợp"),
        ("E", "E. An toàn – Tuân thủ"),
        ("F", "F. Định hướng"),
        ("G", "G. Quản lý")
    ]:
        elements.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
        for k, v in data.items():
            if k.startswith(section):
                elements.append(Paragraph(f"- {k}: {v}", styles["Normal"]))
        elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer

# =========================
# HEADER
# =========================
st.title("✈️ Vietnam Airlines – Khảo sát hệ thống CNTT")
st.caption("Phục vụ Quy hoạch & Đầu tư CNTT 3–5 năm")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "A. Thông tin chung",
    "B. Hạ tầng",
    "C. Dữ liệu",
    "D. Tích hợp",
    "E. An toàn",
    "F. Định hướng",
    "G. Quản lý"
])

# =========================
# TAB A
# =========================
with tabs[0]:
    set_val("A1_SystemName", st.text_input("Tên hệ thống"))
    set_val("A1_SystemCode", st.text_input("Mã hệ thống"))
    set_val("A1_BusinessOwner", st.text_input("Đơn vị nghiệp vụ"))
    set_val("A1_ITOwner", st.text_input("Đơn vị CNTT"))
    set_val("A1_Type", st.multiselect(
        "Loại hệ thống",
        ["COTS", "SaaS", "In-house", "Outsource", "Legacy"]
    ))
    set_val("A2_Objective", st.text_area("Mục tiêu nghiệp vụ"))
    set_val("A3_Status", st.selectbox(
        "Tình trạng",
        ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"]
    ))

# =========================
# TAB B
# =========================
with tabs[1]:
    set_val("B1_Model", st.multiselect(
        "Mô hình hạ tầng",
        ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"]
    ))
    set_val("B2_OS", st.text_input("Hệ điều hành"))
    set_val("B2_DB", st.text_input("Database"))
    set_val("B3_SLA", st.slider("SLA (%)", 90, 100, 99))

# =========================
# TAB C
# =========================
with tabs[2]:
    set_val("C1_PII", st.radio("Có dữ liệu cá nhân?", ["Có", "Không"]))
    set_val("C1_Finance", st.radio("Dữ liệu tài chính?", ["Có", "Không"]))
    set_val("C2_Quality", st.multiselect(
        "Chất lượng dữ liệu",
        ["Đầy đủ", "Chính xác", "Kịp thời"]
    ))

# =========================
# TAB D
# =========================
with tabs[3]:
    set_val("D1_Integration", st.text_area(
        "Hệ thống tích hợp (PSS, DCS, ERP, CRM...)"
    ))
    set_val("D2_Protocol", st.multiselect(
        "Giao thức",
        ["REST", "SOAP", "MQ", "SFTP"]
    ))

# =========================
# TAB E
# =========================
with tabs[4]:
    set_val("E_SSO", st.checkbox("SSO"))
    set_val("E_MFA", st.checkbox("MFA"))
    set_val("E_Compliance", st.multiselect(
        "Tuân thủ",
        ["GDPR", "Luật ATTT VN", "ICAO", "IATA"]
    ))

# =========================
# TAB F
# =========================
with tabs[5]:
    set_val("F_StrategyFit", st.slider("Phù hợp chiến lược số (1–5)", 1, 5, 3))
    set_val("F_Direction", st.radio(
        "Định hướng",
        ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"]
    ))
    set_val("F_Priority", st.radio(
        "Ưu tiên",
        ["High", "Medium", "Low"]
    ))

# =========================
# TAB G
# =========================
with tabs[6]:
    set_val("G_UpdatedBy", st.text_input("Người cập nhật"))
    set_val("G_UpdateDate", datetime.now().strftime("%Y-%m-%d"))
    set_val("G_Note", st.text_area("Ghi chú"))

# =========================
# ACTIONS
# =========================
st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("💾 Lưu JSON"):
        fname = f"{form_data.get('A1_SystemCode','system')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(DATA_DIR, fname), "w", encoding="utf-8") as f:
            json.dump(form_data, f, ensure_ascii=False, indent=2)
        st.success("Đã lưu thành công")

with c2:
    pdf = export_pdf(form_data)
    st.download_button(
        "📄 Xuất PDF A4",
        pdf,
        file_name="IT_Survey.pdf",
        mime="application/pdf"
    )

with c3:
    df = pd.DataFrame([form_data])
    out = BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        "📊 Xuất Excel",
        out.getvalue(),
        file_name="IT_Survey.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =========================
# VIEW SAVED
# =========================
st.subheader("📂 Dữ liệu đã lưu")

files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
for f in sorted(files, reverse=True):
    with st.expander(f):
        with open(os.path.join(DATA_DIR, f), encoding="utf-8") as jf:
            st.json(json.load(jf))
