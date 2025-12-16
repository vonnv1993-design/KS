import streamlit as st
import pandas as pd
import json, os
from datetime import datetime
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="IT Application Survey – Vietnam Airlines",
    layout="wide"
)

DATA_DIR = "data/json"
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# MODERN UI – BRAND STYLE
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(120deg,#F4F7FB,#FFFFFF);
}

h1, h2, h3 {
    color: #005EB8;
    font-weight: 700;
}

.block-container {
    padding-top: 1.5rem;
}

div[data-testid="stTab"] {
    font-weight: 600;
}

div.stButton > button {
    background: linear-gradient(90deg,#FFC72C,#FFB000);
    color: #002B5C;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.5rem 1.2rem;
}

div.stButton > button:hover {
    background: linear-gradient(90deg,#FFD966,#FFC72C);
}

.card {
    background: white;
    padding: 1.2rem;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("✈️ KHẢO SÁT QUY HOẠCH HỆ THỐNG CNTT – VIETNAM AIRLINES")
st.caption("Digital IT Landscape Survey | Enterprise Architecture & IT Master Planning")

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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    system_name = st.text_input("Tên hệ thống / phần mềm")
    system_code = st.text_input("Mã hệ thống (System Code)")
    business_group = st.multiselect(
        "Nhóm nghiệp vụ",
        ["Khai thác bay","Thương mại","Dịch vụ","Kỹ thuật",
         "Tài chính","Nhân sự","An toàn – An ninh","Quản lý chung"]
    )
    business_owner = st.text_input("Business Owner")
    it_owner = st.text_input("IT Owner")
    vendor = st.text_input("Nhà cung cấp / Đối tác")
    system_type = st.multiselect(
        "Loại hệ thống",
        ["COTS","SaaS","In-house","Outsource","Legacy"]
    )
    value_chain = st.multiselect(
        "Vai trò chuỗi giá trị",
        ["Core","Support","Analytics","Compliance"]
    )
    deploy_year = st.selectbox("Năm triển khai", range(2000,2051))
    status = st.radio(
        "Tình trạng hiện tại",
        ["Đang vận hành","Nâng cấp","Thay thế","Dừng"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB B
# =========================
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    infra_model = st.multiselect(
        "Mô hình hạ tầng",
        ["On-Prem","Private Cloud","Public Cloud","Hybrid"]
    )
    dc_region = st.text_input("DC / Cloud Region")
    infra_provider = st.multiselect(
        "Nhà cung cấp hạ tầng",
        ["AWS","Azure","Viettel","VNPT","FPT","Khác"]
    )
    server_type = st.radio("Máy chủ",["VM","Physical"],horizontal=True)
    os_name = st.text_input("Hệ điều hành")
    resource = st.text_input("CPU / RAM / Storage")
    sla = st.slider("SLA (%)",90,100)
    ha_dr = st.multiselect(
        "HA / DR",
        ["Active-Active","Active-Passive","None"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB C
# =========================
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    pii = st.radio("Dữ liệu cá nhân (PII)",["Có","Không"],horizontal=True)
    sensitive = st.radio("Dữ liệu nhạy cảm",["Có","Không"],horizontal=True)
    finance = st.radio("Dữ liệu tài chính",["Có","Không"],horizontal=True)
    cross_border = st.radio("Dữ liệu ra nước ngoài",["Có","Không"],horizontal=True)
    data_source = st.text_input("Source of Truth")
    data_quality = st.multiselect(
        "Chất lượng dữ liệu",
        ["Đầy đủ","Chính xác","Kịp thời"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB D
# =========================
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    integration_desc = st.text_area(
        "Danh sách hệ thống tích hợp",
        placeholder="PSS | Hai chiều | API"
    )
    data_standard = st.multiselect(
        "Chuẩn dữ liệu",
        ["IATA NDC","AIDX","EDIFACT","XML","JSON"]
    )
    protocol = st.multiselect(
        "Giao thức",
        ["REST","SOAP","MQ","SFTP"]
    )
    api_gateway = st.radio("API Gateway",["Có","Không"],horizontal=True)
    logging = st.radio("Logging / Monitoring",["Có","Không"],horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB E
# =========================
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    rbac = st.text_input("Phân quyền truy cập (RBAC)")
    auth = st.multiselect("Xác thực",["SSO","MFA","Khác"])
    legal = st.multiselect(
        "Tuân thủ pháp lý",
        ["GDPR","Luật ATTT VN","ICAO Annex 17","Quy chế ANTT TCTHK"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB F
# =========================
with tabs[5]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    strategy_fit = st.slider("Phù hợp chiến lược số (1–5)",1,5)
    proposal = st.radio(
        "Đề xuất quy hoạch",
        ["Giữ nguyên","Nâng cấp","Hợp nhất","Thay thế"],
        horizontal=True
    )
    priority = st.radio(
        "Độ ưu tiên",
        ["High","Medium","Low"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB G
# =========================
with tabs[6]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    updated_by = st.text_input("Người cập nhật")
    version = st.text_input("Phiên bản form","v1.0")
    note = st.text_area("Ghi chú")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DATA OBJECT
# =========================
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

# =========================
# PDF EXPORT
# =========================
def export_pdf(data: dict):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleCenter",
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=12
    ))

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    def section(title, items):
        elements.append(Paragraph(title, styles["Heading2"]))
        table = Table(
            [[k, str(v)] for k, v in items],
            colWidths=[180, 340]
        )
        elements.append(table)
        elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "BÁO CÁO KHẢO SÁT HỆ THỐNG CNTT – VIETNAM AIRLINES",
        styles["TitleCenter"]
    ))

    section("A. THÔNG TIN CHUNG", [
        ("Tên hệ thống", data["system_name"]),
        ("Mã hệ thống", data["system_code"]),
        ("Nhóm nghiệp vụ", ", ".join(data["business_group"])),
        ("Business Owner", data["business_owner"]),
        ("IT Owner", data["it_owner"]),
        ("Nhà cung cấp", data["vendor"]),
    ])

    elements.append(PageBreak())

    section("B. HẠ TẦNG", [
        ("Mô hình", ", ".join(data["infra_model"])),
        ("DC / Cloud", data["dc_region"]),
        ("Nhà cung cấp", ", ".join(data["infra_provider"])),
        ("SLA", f'{data["sla"]}%'),
    ])

    elements.append(PageBreak())

    section("C. DỮ LIỆU & D. TÍCH HỢP", [
        ("PII", data["pii"]),
        ("Dữ liệu nhạy cảm", data["sensitive"]),
        ("Tích hợp", data["integration"]),
    ])

    elements.append(PageBreak())

    section("E–G. ĐỊNH HƯỚNG & QUẢN LÝ", [
        ("Phù hợp chiến lược", data["strategy_fit"]),
        ("Đề xuất", data["proposal"]),
        ("Ưu tiên", data["priority"]),
        ("Người cập nhật", data["updated_by"]),
        ("Ngày cập nhật", data["updated_date"]),
    ])

    doc.build(elements)
    return buffer.getvalue()

# =========================
# ACTIONS
# =========================
st.divider()
c1, c2 = st.columns(2)

with c1:
    if st.button("💾 Lưu JSON theo đơn vị"):
        name = system_code or "system"
        fname = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(DATA_DIR, fname), "w", encoding="utf-8") as f:
            json.dump(form_data, f, ensure_ascii=False, indent=2)
        st.success("Đã lưu JSON thành công")

with c2:
    pdf_bytes = export_pdf(form_data)
    st.download_button(
        "📄 Xuất PDF A4 (4 trang)",
        pdf_bytes,
        file_name="IT_Survey_Vietnam_Airlines.pdf",
        mime="application/pdf"
    )
