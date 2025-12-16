import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

st.set_page_config(page_title="Khảo sát quy hoạch hệ thống CNTT hàng không", layout="wide")

st.title("📋 KHẢO SÁT QUY HOẠCH HỆ THỐNG PHẦN MỀM HÀNG KHÔNG")

# ======================
# A. THÔNG TIN CHUNG
# ======================
st.header("A. THÔNG TIN CHUNG")

with st.expander("A1. Thông tin định danh hệ thống", expanded=True):
    system_name = st.text_input("Tên hệ thống/phần mềm")
    system_code = st.text_input("Mã hệ thống (System Code)")
    business_group = st.multiselect(
        "Nhóm nghiệp vụ",
        ["Khai thác bay", "Thương mại", "Dịch vụ", "Kỹ thuật", "Tài chính", "Nhân sự", "An toàn – An ninh", "Quản lý chung"]
    )
    business_owner = st.text_input("Đơn vị sở hữu nghiệp vụ (Business Owner)")
    it_owner = st.text_input("Đơn vị quản lý CNTT (IT Owner)")
    vendor = st.text_input("Nhà cung cấp / Đối tác")
    system_type = st.multiselect("Loại hệ thống", ["COTS", "SaaS", "In-house", "Outsource", "Legacy"])
    value_chain_role = st.multiselect("Vai trò trong chuỗi giá trị", ["Core", "Support", "Analytics", "Compliance"])

with st.expander("A2. Mục tiêu & phạm vi"):
    business_goal = st.text_area("Mục tiêu nghiệp vụ chính")
    scope = st.text_area("Phạm vi chức năng")
    users = st.text_input("Đối tượng người dùng")
    user_scale = st.radio("Số lượng user", ["<10", "10–50", "50–100", ">100"])
    region = st.multiselect("Khu vực sử dụng", ["Nội địa", "Quốc tế", "Toàn mạng"])

with st.expander("A3. Tình trạng & vòng đời"):
    deploy_year = st.selectbox("Năm triển khai", list(range(2000, 2051)))
    status = st.radio("Tình trạng hiện tại", ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"])
    business_fit = st.slider("Mức độ đáp ứng nghiệp vụ (1–5)", 1, 5)
    plan_3_5y = st.multiselect("Kế hoạch 3–5 năm", ["Giữ nguyên", "Nâng cấp", "Thay thế", "Hợp nhất"])

# ======================
# B. HẠ TẦNG
# ======================
st.header("B. HẠ TẦNG (INFRASTRUCTURE)")

infra_model = st.multiselect("Mô hình hạ tầng", ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"])
dc_location = st.text_input("Vị trí DC/Cloud Region")
infra_provider = st.multiselect("Nhà cung cấp hạ tầng", ["AWS", "Azure", "Viettel", "VNPT", "FPT", "Khác"])

server_type = st.radio("Máy chủ", ["VM", "Physical"])
os = st.text_input("Hệ điều hành")
resource = st.text_input("CPU / RAM / Storage")
db_engine = st.text_input("Database Engine")
middleware = st.text_input("Middleware")
network = st.text_input("Network")

sla = st.slider("SLA (%)", 90, 100)
ha_dr = st.multiselect("HA / DR", ["Active-Active", "Active-Passive", "None"])
backup = st.multiselect("Sao lưu dữ liệu", ["Hàng ngày", "Thời gian thực"])
standards = st.multiselect("Tuân thủ tiêu chuẩn", ["ISO 27001", "PCI DSS", "ICAO", "IATA"])

# ======================
# C. DỮ LIỆU
# ======================
st.header("C. DỮ LIỆU (DATA)")

pii = st.radio("Dữ liệu cá nhân (PII)", ["Có", "Không"])
sensitive = st.radio("Dữ liệu nhạy cảm/an ninh", ["Có", "Không"])
finance_data = st.radio("Dữ liệu tài chính", ["Có", "Không"])
cross_border = st.radio("Dữ liệu có rời Việt Nam", ["Có", "Không"])
core_data_desc = st.text_area("Dữ liệu nghiệp vụ chính & nhạy cảm")

data_format = st.multiselect("Định dạng dữ liệu", ["Structured", "Semi-structured", "Unstructured"])
data_quality = st.multiselect("Chất lượng dữ liệu", ["Đầy đủ", "Chính xác", "Kịp thời"])

bi_ai = st.radio("Cung cấp dữ liệu cho BI/AI", ["Có", "Không"])
real_time = st.radio("Dữ liệu thời gian thực", ["Có", "Không"])

# ======================
# D. TÍCH HỢP
# ======================
st.header("D. TÍCH HỢP / CHIA SẺ")

integration_systems = st.text_area(
    "Danh sách hệ thống tích hợp (Tên – Vai trò – Hình thức)",
    placeholder="VD: PSS | Hai chiều | API"
)

standards_data = st.multiselect("Chuẩn dữ liệu", ["IATA NDC", "AIDX", "EDIFACT", "XML", "JSON", "Khác"])
protocols = st.multiselect("Giao thức", ["REST", "SOAP", "MQ", "SFTP"])

api_gateway = st.radio("Có API Gateway", ["Có", "Không"])
logging = st.radio("Logging / Monitoring", ["Có", "Không"])

# ======================
# E. AN TOÀN – TUÂN THỦ
# ======================
st.header("E. AN TOÀN – TUÂN THỦ")

rbac = st.text_input("Phân quyền (RBAC)")
auth = st.multiselect("Xác thực", ["SSO", "MFA", "Khác"])
legal = st.multiselect("Tuân thủ pháp lý", ["GDPR", "Luật ATTT VN", "ICAO Annex 17", "Quy chế ANTT TCTHK"])

# ======================
# F. ĐÁNH GIÁ & ĐỊNH HƯỚNG
# ======================
st.header("F. ĐÁNH GIÁ & ĐỊNH HƯỚNG")

strategy_fit = st.slider("Phù hợp chiến lược số (1–5)", 1, 5)
proposal = st.radio("Đề xuất", ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"])
priority = st.radio("Độ ưu tiên", ["High", "Medium", "Low"])

# ======================
# G. QUẢN LÝ
# ======================
st.header("G. QUẢN LÝ – LƯU TRỮ")

updated_by = st.text_input("Người cập nhật")
updated_date = datetime.now().strftime("%d/%m/%Y")
version = st.text_input("Phiên bản form", "v1.0")
note = st.text_area("Ghi chú")

# ======================
# LƯU & XUẤT
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

col1, col2 = st.columns(2)

with col1:
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    st.download_button(
        "⬇️ Xuất Excel",
        excel_buffer.getvalue(),
        file_name="khao_sat_he_thong_cntt.xlsx"
    )

with col2:
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph("<b>BÁO CÁO KHẢO SÁT HỆ THỐNG CNTT</b>", styles["Title"]), Spacer(1, 12)]

    table_data = [[k, v] for k, v in data.items()]
    table = Table(table_data, colWidths=[200, 300])
    elements.append(table)
    doc.build(elements)

    st.download_button(
        "⬇️ Xuất PDF",
        pdf_buffer.getvalue(),
        file_name="bao_cao_khao_sat_he_thong.pdf"
    )
