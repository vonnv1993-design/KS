import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="IT Application Survey – Vietnam Airlines",
    layout="wide"
)

DATA_DIR = "data/json"
EXCEL_DIR = "data/excel"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)

# ======================
# BRAND STYLE
# ======================
st.markdown("""
<style>
body {
    background-color: #0B2A4A;
}
section[data-testid="stSidebar"] {
    background-color: #003A8F;
}
h1, h2, h3 {
    color: #005EB8;
}
div.stButton > button {
    background-color: #FFC72C;
    color: black;
    border-radius: 6px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("✈️ KHẢO SÁT QUY HOẠCH HỆ THỐNG CNTT – VIETNAM AIRLINES")

# ======================
# SESSION INIT
# ======================
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# ======================
# TABS
# ======================
tabA, tabB, tabC, tabD, tabE, tabF, tabG = st.tabs(
    ["A. Thông tin chung", "B. Hạ tầng", "C. Dữ liệu",
     "D. Tích hợp", "E. An toàn", "F. Định hướng", "G. Quản lý"]
)

# ======================
# TAB A
# ======================
with tabA:
    st.subheader("A. THÔNG TIN CHUNG")
    system_name = st.text_input("Tên hệ thống")
    system_code = st.text_input("Mã hệ thống")
    business_group = st.multiselect(
        "Nhóm nghiệp vụ",
        ["Khai thác bay", "Thương mại", "Dịch vụ", "Kỹ thuật",
         "Tài chính", "Nhân sự", "An toàn – An ninh", "Quản lý chung"]
    )
    business_owner = st.text_input("Business Owner")
    it_owner = st.text_input("IT Owner")
    vendor = st.text_input("Nhà cung cấp")
    system_type = st.multiselect(
        "Loại hệ thống",
        ["COTS", "SaaS", "In-house", "Outsource", "Legacy"]
    )
    value_chain = st.multiselect(
        "Vai trò chuỗi giá trị",
        ["Core", "Support", "Analytics", "Compliance"]
    )
    deploy_year = st.selectbox("Năm triển khai", range(2000, 2051))
    status = st.radio("Tình trạng", ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"])

# ======================
# TAB B
# ======================
with tabB:
    st.subheader("B. HẠ TẦNG")
    infra_model = st.multiselect(
        "Mô hình triển khai",
        ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"]
    )
    dc_region = st.text_input("DC / Cloud Region")
    infra_provider = st.multiselect(
        "Nhà cung cấp",
        ["AWS", "Azure", "Viettel", "VNPT", "FPT", "Khác"]
    )
    server_type = st.radio("Máy chủ", ["VM", "Physical"])
    os_name = st.text_input("Hệ điều hành")
    resource = st.text_input("CPU / RAM / Storage")
    sla = st.slider("SLA (%)", 90, 100)
    ha_dr = st.multiselect("HA / DR", ["Active-Active", "Active-Passive", "None"])

# ======================
# TAB C
# ======================
with tabC:
    st.subheader("C. DỮ LIỆU")
    pii = st.radio("PII", ["Có", "Không"])
    sensitive = st.radio("Dữ liệu nhạy cảm", ["Có", "Không"])
    finance = st.radio("Dữ liệu tài chính", ["Có", "Không"])
    cross_border = st.radio("Dữ liệu ra nước ngoài", ["Có", "Không"])
    data_source = st.text_input("Source of Truth")
    data_quality = st.multiselect(
        "Chất lượng dữ liệu",
        ["Đầy đủ", "Chính xác", "Kịp thời"]
    )

# ======================
# TAB D
# ======================
with tabD:
    st.subheader("D. TÍCH HỢP")
    integration_desc = st.text_area(
        "Danh sách hệ thống tích hợp",
        placeholder="PSS | Hai chiều | API"
    )
    data_standard = st.multiselect(
        "Chuẩn dữ liệu",
        ["IATA NDC", "AIDX", "EDIFACT", "XML", "JSON"]
    )
    protocol = st.multiselect(
        "Giao thức",
        ["REST", "SOAP", "MQ", "SFTP"]
    )
    api_gateway = st.radio("API Gateway", ["Có", "Không"])
    logging = st.radio("Logging / Monitoring", ["Có", "Không"])

# ======================
# TAB E
# ======================
with tabE:
    st.subheader("E. AN TOÀN – TUÂN THỦ")
    rbac = st.text_input("RBAC")
    auth = st.multiselect("Xác thực", ["SSO", "MFA", "Khác"])
    legal = st.multiselect(
        "Tuân thủ",
        ["GDPR", "Luật ATTT VN", "ICAO Annex 17", "Quy chế ANTT TCTHK"]
    )

# ======================
# TAB F
# ======================
with tabF:
    st.subheader("F. ĐỊNH HƯỚNG")
    strategy_fit = st.slider("Phù hợp chiến lược (1–5)", 1, 5)
    proposal = st.radio(
        "Đề xuất",
        ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"]
    )
    priority = st.radio("Ưu tiên", ["High", "Medium", "Low"])

# ======================
# TAB G
# ======================
with tabG:
    st.subheader("G. QUẢN LÝ")
    updated_by = st.text_input("Người cập nhật")
    version = st.text_input("Phiên bản", "v1.0")
    note = st.text_area("Ghi chú")

# ======================
# SAVE DATA
# ======================
form_data = {
    "system_name": system_name,
    "system_code": system_code,
    "business_group": business_group,
    "business_owner": business_owner,
    "it_owner": it_owner,
    "vendor": vendor,
    "system_type": system_type,
    "value_chain": value_chain,
    "deploy_year": deploy_year,
    "status": status,
    "infra_model": infra_model,
    "dc_region": dc_region,
    "infra_provider": infra_provider,
    "sla": sla,
    "pii": pii,
    "sensitive": sensitive,
    "finance": finance,
    "cross_border": cross_border,
    "integration": integration_desc,
    "strategy_fit": strategy_fit,
    "proposal": proposal,
    "priority": priority,
    "updated_by": updated_by,
    "updated_date": datetime.now().strftime("%d/%m/%Y"),
    "version": version,
    "note": note
}

# ======================
# ACTION BUTTONS
# ======================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Lưu JSON theo đơn vị"):
        filename = f"{system_code or 'system'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
            json.dump(form_data, f, ensure_ascii=False, indent=2)
        st.success("Đã lưu JSON thành công")

with col2:
    if st.button("📊 Xuất Excel Master"):
        files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
        rows = []
        for file in files:
            with open(os.path.join(DATA_DIR, file), encoding="utf-8") as f:
                rows.append(json.load(f))
        df = pd.DataFrame(rows)
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button(
            "⬇️ Tải Excel",
            buffer.getvalue(),
            "IT_Survey_Master.xlsx"
        )

with col3:
    st.info("PDF A4 chuẩn in: dùng module riêng (next step)")

