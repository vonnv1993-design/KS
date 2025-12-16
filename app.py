import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Khảo sát quy hoạch hệ thống CNTT hàng không",
    layout="wide"
)

# ======================
# FLAT UI CSS
# ======================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
}
h1, h2, h3 {
    font-weight: 600;
}
.section-card {
    background: #ffffff;
    padding: 20px 24px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 24px;
}
.stDownloadButton button, .stButton button {
    border-radius: 10px;
    height: 42px;
    font-weight: 600;
}
div[data-baseweb="input"],
div[data-baseweb="select"],
div[data-baseweb="textarea"] {
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown("""
## 📋 Khảo sát Quy hoạch Hệ thống CNTT Hàng không
<span style="color:#6b7280">
Chuẩn hóa danh mục hệ thống – Đánh giá hiện trạng – Định hướng đầu tư CNTT 3–5 năm
</span>
""", unsafe_allow_html=True)

st.divider()

# ======================
# A. THÔNG TIN CHUNG
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("A. THÔNG TIN CHUNG")

st.markdown("**A1. Thông tin định danh hệ thống**")
c1, c2 = st.columns(2)
with c1:
    system_name = st.text_input("Tên hệ thống/phần mềm", placeholder="VD: Crew Management System")
    system_code = st.text_input("Mã hệ thống", placeholder="VD: CMS-001")
    business_owner = st.text_input("Business Owner")
with c2:
    it_owner = st.text_input("IT Owner")
    vendor = st.text_input("Nhà cung cấp / Đối tác")
    system_type = st.multiselect(
        "Loại hệ thống", ["COTS", "SaaS", "In-house", "Outsource", "Legacy"]
    )

business_group = st.multiselect(
    "Nhóm nghiệp vụ",
    ["Khai thác bay", "Thương mại", "Dịch vụ", "Kỹ thuật", "Tài chính",
     "Nhân sự", "An toàn – An ninh", "Quản lý chung"]
)

value_chain_role = st.multiselect(
    "Vai trò trong chuỗi giá trị", ["Core", "Support", "Analytics", "Compliance"]
)

st.markdown("**A2. Mục tiêu & phạm vi**")
business_goal = st.text_area("Mục tiêu nghiệp vụ chính")
scope = st.text_area("Phạm vi chức năng")
users = st.text_input("Đối tượng người dùng")
user_scale = st.radio(
    "Quy mô người dùng",
    ["<10", "10–50", "50–100", ">100"],
    horizontal=True
)
region = st.multiselect("Khu vực sử dụng", ["Nội địa", "Quốc tế", "Toàn mạng"])

st.markdown("**A3. Tình trạng & vòng đời**")
c1, c2, c3 = st.columns(3)
with c1:
    deploy_year = st.selectbox("Năm triển khai", list(range(2000, 2051)))
with c2:
    status = st.selectbox(
        "Tình trạng hiện tại",
        ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"]
    )
with c3:
    business_fit = st.slider("Đáp ứng nghiệp vụ", 1, 5)

plan_3_5y = st.radio(
    "Kế hoạch 3–5 năm",
    ["Giữ nguyên", "Nâng cấp", "Thay thế", "Hợp nhất"],
    horizontal=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# B. HẠ TẦNG
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("B. HẠ TẦNG (INFRASTRUCTURE)")

infra_model = st.multiselect(
    "Mô hình hạ tầng", ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"]
)
dc_location = st.text_input("Vị trí DC / Cloud Region")
infra_provider = st.multiselect(
    "Nhà cung cấp hạ tầng", ["AWS", "Azure", "Viettel", "VNPT", "FPT", "Khác"]
)

c1, c2 = st.columns(2)
with c1:
    server_type = st.radio("Máy chủ", ["VM", "Physical"], horizontal=True)
    os = st.text_input("Hệ điều hành")
    resource = st.text_input("CPU / RAM / Storage")
with c2:
    db_engine = st.text_input("Database Engine")
    middleware = st.text_input("Middleware")
    network = st.text_input("Network")

sla = st.slider("SLA (%)", 90, 100)
ha_dr = st.multiselect("HA / DR", ["Active-Active", "Active-Passive", "None"])
backup = st.multiselect("Sao lưu dữ liệu", ["Hàng ngày", "Thời gian thực"])
standards = st.multiselect(
    "Tuân thủ tiêu chuẩn", ["ISO 27001", "PCI DSS", "ICAO", "IATA"]
)
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# C. DỮ LIỆU
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("C. DỮ LIỆU (DATA)")

c1, c2, c3, c4 = st.columns(4)
with c1:
    pii = st.radio("PII", ["Có", "Không"], horizontal=True)
with c2:
    sensitive = st.radio("Dữ liệu nhạy cảm", ["Có", "Không"], horizontal=True)
with c3:
    finance_data = st.radio("Tài chính", ["Có", "Không"], horizontal=True)
with c4:
    cross_border = st.radio("Dữ liệu ra nước ngoài", ["Có", "Không"], horizontal=True)

core_data_desc = st.text_area("Mô tả dữ liệu nghiệp vụ & trọng yếu")

data_format = st.multiselect(
    "Định dạng dữ liệu", ["Structured", "Semi-structured", "Unstructured"]
)
data_quality = st.multiselect(
    "Chất lượng dữ liệu", ["Đầy đủ", "Chính xác", "Kịp thời"]
)

bi_ai = st.radio("Cung cấp cho BI / AI", ["Có", "Không"], horizontal=True)
real_time = st.radio("Dữ liệu thời gian thực", ["Có", "Không"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# D. TÍCH HỢP
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("D. TÍCH HỢP / CHIA SẺ")

integration_systems = st.text_area(
    "Danh sách hệ thống tích hợp (Tên | Vai trò | Hình thức)",
    placeholder="VD: PSS | Hai chiều | API"
)

standards_data = st.multiselect(
    "Chuẩn dữ liệu", ["IATA NDC", "AIDX", "EDIFACT", "XML", "JSON", "Khác"]
)
protocols = st.multiselect(
    "Giao thức", ["REST", "SOAP", "MQ", "SFTP"]
)

c1, c2 = st.columns(2)
with c1:
    api_gateway = st.radio("API Gateway", ["Có", "Không"], horizontal=True)
with c2:
    logging = st.radio("Logging / Monitoring", ["Có", "Không"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# E. AN TOÀN – TUÂN THỦ
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("E. AN TOÀN – TUÂN THỦ")

rbac = st.text_input("Phân quyền (RBAC)")
auth = st.multiselect("Xác thực", ["SSO", "MFA", "Khác"])
legal = st.multiselect(
    "Tuân thủ pháp lý",
    ["GDPR", "Luật ATTT VN", "ICAO Annex 17", "Quy chế ANTT TCTHK"]
)
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# F. ĐÁNH GIÁ & ĐỊNH HƯỚNG
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("F. ĐÁNH GIÁ & ĐỊNH HƯỚNG")

strategy_fit = st.slider("Phù hợp chiến lược số", 1, 5)
proposal = st.radio(
    "Đề xuất",
    ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"],
    horizontal=True
)
priority = st.radio(
    "Độ ưu tiên",
    ["High", "Medium", "Low"],
    horizontal=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# G. QUẢN LÝ
# ======================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("G. QUẢN LÝ – LƯU TRỮ")

updated_by = st.text_input("Người cập nhật")
updated_date = datetime.now().strftime("%d/%m/%Y")
version = st.text_input("Phiên bản form", "v1.0")
note = st.text_area("Ghi chú")
st.markdown('</div>', unsafe_allow_html=True)

# ======================
# EXPORT
# ======================
data = {
    "Tên hệ thống": system_name,
    "Mã hệ thống": system_code,
    "Nhóm nghiệp vụ": ", ".join(business_group),
    "Business Owner": business_owner,
    "IT Owner": it_owner,
    "Nhà cung cấp": vendor,
    "Loại hệ thống": ", ".join(system_type),
    "Vai trò chuỗi giá trị": ", ".join(value_chain_role),
    "Mục tiêu": business_goal,
    "Năm triển khai": deploy_year,
    "Tình trạng": status,
    "Phù hợp chiến lược": strategy_fit,
    "Đề xuất": proposal,
    "Ưu tiên": priority,
    "Người cập nhật": updated_by,
    "Ngày cập nhật": updated_date
}

df = pd.DataFrame([data])

excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False)

pdf_buffer = BytesIO()
doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
styles = getSampleStyleSheet()
elements = [
    Paragraph("<b>BÁO CÁO KHẢO SÁT HỆ THỐNG CNTT</b>", styles["Title"]),
    Spacer(1, 12),
    Table([[k, v] for k, v in data.items()], colWidths=[200, 300])
]
doc.build(elements)

st.divider()
st.subheader("📤 Xuất dữ liệu")

c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "⬇️ Xuất Excel",
        excel_buffer.getvalue(),
        "khao_sat_he_thong_cntt.xlsx",
        use_container_width=True
    )
with c2:
    st.download_button(
        "⬇️ Xuất PDF",
        pdf_buffer.getvalue(),
        "bao_cao_khao_sat_he_thong.pdf",
        use_container_width=True
    )
