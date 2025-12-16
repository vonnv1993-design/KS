import json
import uuid
from datetime import datetime, date
from typing import Any, Dict

import pandas as pd
import streamlit as st


# =========================
# Helpers
# =========================
def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def required(value: str) -> bool:
    return bool(value and str(value).strip())


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dict to 1-level dict for CSV export / Google Sheets row."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.append((new_key, ", ".join([str(x) for x in v])))
        else:
            items.append((new_key, v))
    return dict(items)


def build_record(form: Dict[str, Any]) -> Dict[str, Any]:
    """Add system fields for tracking."""
    record = {
        "_meta": {
            "record_id": str(uuid.uuid4()),
            "created_at": now_iso(),
            "app": "it-survey-streamlit",
            "schema_version": "1.0",
        },
        "form": form,
    }
    return record


# =========================
# Optional: Google Sheets
# =========================
def save_to_gsheets(record: Dict[str, Any]) -> None:
    """
    Save a record to Google Sheets.
    Requirements in Streamlit secrets:
      - st.secrets["gcp_service_account"] : service account json object
      - st.secrets["gsheets"]["spreadsheet_id"]
      - st.secrets["gsheets"]["worksheet_name"] (optional; default 'data')
    """
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    gc = gspread.authorize(creds)

    spreadsheet_id = st.secrets["gsheets"]["spreadsheet_id"]
    worksheet_name = st.secrets["gsheets"].get("worksheet_name", "data")

    sh = gc.open_by_key(spreadsheet_id)
    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows=2000, cols=200)

    flat = flatten_dict(record)

    # If sheet empty -> create header row
    existing_headers = ws.row_values(1)
    if not existing_headers:
        ws.append_row(list(flat.keys()))
        ws.append_row(list(flat.values()))
        return

    # If new keys appear -> extend header
    headers = existing_headers[:]
    changed = False
    for k in flat.keys():
        if k not in headers:
            headers.append(k)
            changed = True

    if changed:
        ws.update("1:1", [headers])

    row = [flat.get(h, "") for h in headers]
    ws.append_row(row)


# =========================
# UI
# =========================
st.set_page_config(page_title="Khảo sát hệ thống CNTT", layout="wide")

st.title("Tool số hóa form khảo sát hệ thống CNTT")
st.caption("Nhập theo các mục A→G. Có thể tải JSON/CSV hoặc lưu vào Google Sheets (khuyến nghị khi deploy Cloud).")

with st.sidebar:
    st.header("Thiết lập lưu dữ liệu")
    save_mode = st.radio(
        "Chế độ lưu",
        options=["Chỉ tải về (JSON/CSV)", "Lưu Google Sheets"],
        index=0,
    )
    st.info(
        "Trên Streamlit Cloud, lưu file vào máy chủ không bền vững. "
        "Nếu muốn lưu tập trung, hãy chọn Google Sheets."
    )

tabs = st.tabs([
    "A. Tổng quan",
    "B. Hạ tầng",
    "C. Dữ liệu",
    "D. Tích hợp",
    "E. An toàn – Tuân thủ",
    "F. Đánh giá & Định hướng",
    "G. Quản lý – Lưu trữ",
    "Submit / Xuất / Lưu",
])

# Keep last submission in session
if "last_record" not in st.session_state:
    st.session_state.last_record = None


with st.form("survey_form", clear_on_submit=False):

    # ----------------------------
    # A. Tổng quan
    # ----------------------------
    with tabs[0]:
        st.subheader("A. THÔNG TIN TỔNG QUAN, CHUNG")

        st.markdown("### A1. Thông tin định danh hệ thống")
        col1, col2 = st.columns(2)
        with col1:
            system_name = st.text_input("Tên hệ thống/phần mềm *")
            system_code = st.text_input("Mã hệ thống (System Code) *")
            business_group = st.selectbox(
                "Nhóm nghiệp vụ",
                options=[
                    "Khai thác bay", "Bán – Thương mại", "Khách hàng", "Bảo dưỡng",
                    "Tài chính", "Nhân sự", "An toàn – An ninh", "Khác"
                ],
            )
            business_owner = st.text_input("Đơn vị sở hữu nghiệp vụ (Business Owner)")
        with col2:
            it_owner = st.text_input("Đơn vị quản lý CNTT (IT Owner)")
            vendor_partner = st.text_input("Nhà cung cấp / Đối tác")
            system_type = st.multiselect(
                "Loại hệ thống",
                options=["COTS", "SaaS", "In-house", "Outsource", "Legacy"],
            )
            value_chain_role = st.multiselect(
                "Vai trò trong chuỗi giá trị hàng không",
                options=["Core", "Support", "Analytics", "Compliance"],
            )

        st.markdown("### A2. Mục tiêu & phạm vi")
        col1, col2 = st.columns(2)
        with col1:
            business_goal = st.text_area("Mục tiêu nghiệp vụ chính", height=90)
            functional_scope = st.text_area("Phạm vi chức năng", height=90)
        with col2:
            user_audience = st.text_area("Đối tượng người dùng", height=90)
            user_count_current = st.number_input("Số lượng user (hiện tại)", min_value=0, step=1)
            user_count_forecast = st.number_input("Số lượng user (dự kiến 3–5 năm)", min_value=0, step=1)
            usage_region = st.multiselect("Khu vực sử dụng", options=["Nội địa", "Quốc tế", "Toàn mạng"])

        st.markdown("### A3. Tình trạng & vòng đời")
        col1, col2, col3 = st.columns(3)
        with col1:
            deployment_year = st.number_input("Năm triển khai", min_value=1980, max_value=2100, step=1, value=2020)
            current_status = st.radio("Tình trạng hiện tại", options=["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"])
        with col2:
            business_fit_score = st.slider("Đánh giá mức độ đáp ứng nghiệp vụ (1–5)", 1, 5, 3)
        with col3:
            plan_3_5y = st.radio("Kế hoạch 3–5 năm", options=["Giữ nguyên", "Nâng cấp", "Thay thế", "Hợp nhất"])

    # ----------------------------
    # B. Hạ tầng
    # ----------------------------
    with tabs[1]:
        st.subheader("B. THÔNG TIN VỀ HẠ TẦNG (INFRASTRUCTURE)")

        st.markdown("### B1. Mô hình triển khai")
        infra_model = st.radio("Mô hình hạ tầng", options=["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"])
        dc_region = st.text_input("Vị trí DC/Cloud Region")
        infra_provider = st.text_input("Nhà cung cấp hạ tầng (AWS/Azure/GCP/IDC…)")

        st.markdown("### B2. Tài nguyên hạ tầng")
        col1, col2 = st.columns(2)
        with col1:
            servers = st.text_area("Máy chủ (VM/Physical)", height=80)
            os_info = st.text_input("Hệ điều hành")
            cpu_ram_storage = st.text_input("CPU / RAM / Storage")
        with col2:
            db_engine = st.text_input("Database Engine")
            middleware = st.text_input("Middleware")
            network = st.text_input("Network (LAN/WAN/MPLS/VPN)")

        st.markdown("### B3. Tính sẵn sàng & an toàn")
        col1, col2, col3 = st.columns(3)
        with col1:
            sla_uptime = st.text_input("SLA (% uptime)", placeholder="Ví dụ: 99.9%")
            ha_dr = st.radio("HA/DR", options=["Active-Active", "Active-Passive", "None"])
        with col2:
            rpo = st.text_input("RPO", placeholder="Ví dụ: 15 phút / 1 giờ")
            rto = st.text_input("RTO", placeholder="Ví dụ: 2 giờ")
        with col3:
            backup = st.radio("Sao lưu dữ liệu", options=["Hàng ngày", "Thời gian thực"])
            compliance = st.multiselect(
                "Tuân thủ tiêu chuẩn",
                options=["ISO 27001", "PCI DSS", "ICAO", "IATA", "An ninh HK"],
            )

    # ----------------------------
    # C. Dữ liệu
    # ----------------------------
    with tabs[2]:
        st.subheader("C. THÔNG TIN VỀ DỮ LIỆU (DATA)")

        st.markdown("### C1. Loại dữ liệu")
        main_business_data = st.text_area("Dữ liệu nghiệp vụ chính", height=80)
        pii = st.radio("Dữ liệu cá nhân (PII)", options=["Có", "Không"])
        sensitive_aviation = st.text_area("Dữ liệu nhạy cảm / an ninh hàng không", height=80)
        financial_payment = st.text_area("Dữ liệu tài chính / thanh toán", height=80)

        st.markdown("### C2. Quản lý & chất lượng dữ liệu")
        col1, col2 = st.columns(2)
        with col1:
            source_of_truth = st.text_input("Nguồn dữ liệu (Source of Truth)")
            data_format = st.selectbox("Định dạng dữ liệu", options=["Structured", "Semi", "Unstructured"])
            data_volume = st.text_input("Dung lượng dữ liệu (hiện tại / tăng trưởng năm)", placeholder="Ví dụ: 2TB / +20%/năm")
        with col2:
            retention_policy = st.text_area("Chính sách lưu trữ & xóa dữ liệu", height=80)
            data_quality = st.multiselect("Chất lượng dữ liệu", options=["Đầy đủ", "Chính xác", "Kịp thời"])

        st.markdown("### C3. Khai thác & phân tích")
        bi_ai = st.radio("Có cung cấp dữ liệu cho BI/AI không?", options=["Có", "Không"])
        dwh_datalake = st.text_input("Kết nối Data Warehouse / Data Lake")
        sync_frequency = st.text_input("Tần suất đồng bộ dữ liệu", placeholder="Ví dụ: 5 phút / hàng ngày / batch")
        realtime_data = st.radio("Dữ liệu thời gian thực (Real-time)", options=["Có", "Không"])

    # ----------------------------
    # D. Tích hợp
    # ----------------------------
    with tabs[3]:
        st.subheader("D. THÔNG TIN VỀ CÔNG NGHỆ TÍCH HỢP / CHIA SẺ")

        st.markdown("### D1. Tích hợp hệ thống")
        related_systems = st.text_area(
            "Các hệ thống liên quan (PSS, DCS, MRO, CRM, ERP, Contact Center…)",
            height=80,
        )
        integration_role = st.radio("Vai trò", options=["Gửi", "Nhận", "Hai chiều"])
        integration_method = st.multiselect("Hình thức tích hợp", options=["API", "ESB", "Message Queue", "File", "Manual"])

        st.markdown("### D2. Chuẩn & giao thức")
        data_standard = st.multiselect("Chuẩn dữ liệu", options=["IATA NDC", "AIDX", "EDIFACT", "XML", "JSON"])
        protocol = st.multiselect("Giao thức", options=["REST", "SOAP", "MQ", "SFTP"])
        integration_frequency = st.radio("Tần suất tích hợp", options=["Real-time", "Near real-time", "Batch"])

        st.markdown("### D3. Quản trị tích hợp")
        api_gateway = st.radio("Có API Gateway không?", options=["Có", "Không"])
        logging_monitoring = st.radio("Có logging / monitoring không?", options=["Có", "Không"])
        api_versioning = st.text_input("Quản lý version API", placeholder="Ví dụ: v1/v2; semantic versioning; header-based…")
        dependency_level = st.radio("Mức độ phụ thuộc hệ thống khác", options=["Low", "Medium", "High"])

    # ----------------------------
    # E. An toàn – Tuân thủ
    # ----------------------------
    with tabs[4]:
        st.subheader("E. THÔNG TIN AN TOÀN – TUÂN THỦ (KHUYẾN NGHỊ)")
        rbac = st.text_area("Phân quyền truy cập (RBAC)", height=80)
        auth = st.multiselect("Xác thực", options=["SSO", "MFA"])
        encryption = st.multiselect("Mã hóa dữ liệu", options=["At-rest", "In-transit"])
        legal_compliance = st.multiselect("Tuân thủ pháp lý", options=["GDPR", "Luật ATTT VN", "ICAO Annex 17"])

    # ----------------------------
    # F. Đánh giá & Định hướng
    # ----------------------------
    with tabs[5]:
        st.subheader("F. ĐÁNH GIÁ & ĐỊNH HƯỚNG QUY HOẠCH")
        col1, col2 = st.columns(2)
        with col1:
            digital_strategy_fit = st.slider("Mức độ phù hợp chiến lược số (1–5)", 1, 5, 3)
            cloud_ai_readiness = st.selectbox("Mức độ sẵn sàng Cloud / AI", options=["Thấp", "Trung bình", "Cao"])
        with col2:
            scalability = st.selectbox("Khả năng mở rộng (Scalability)", options=["Thấp", "Trung bình", "Cao"])

        recommendation = st.radio("Đề xuất", options=["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"])
        priority = st.radio("Độ ưu tiên", options=["High", "Medium", "Low"])

    # ----------------------------
    # G. Quản lý – Lưu trữ
    # ----------------------------
    with tabs[6]:
        st.subheader("G. THÔNG TIN QUẢN LÝ – LƯU TRỮ")
        updated_by = st.text_input("Người cập nhật *")
        updated_date = st.date_input("Ngày cập nhật", value=date.today())
        form_version = st.text_input("Phiên bản form", value="1.0")
        notes = st.text_area("Ghi chú", height=90)

    # ----------------------------
    # Submit
    # ----------------------------
    with tabs[7]:
        st.subheader("Submit / Xuất / Lưu")
        st.write("Nhấn **Submit** để chốt dữ liệu, sau đó tải JSON/CSV hoặc lưu Google Sheets.")
        submitted = st.form_submit_button("Submit", type="primary")


# =========================
# After submit
# =========================
if submitted:
    errors = []
    if not required(system_name):
        errors.append("Thiếu: Tên hệ thống/phần mềm")
    if not required(system_code):
        errors.append("Thiếu: Mã hệ thống (System Code)")
    if not required(updated_by):
        errors.append("Thiếu: Người cập nhật")

    if errors:
        st.error("Vui lòng bổ sung trường bắt buộc:\n- " + "\n- ".join(errors))
        st.stop()

    form_data: Dict[str, Any] = {
        "A": {
            "A1": {
                "system_name": system_name,
                "system_code": system_code,
                "business_group": business_group,
                "business_owner": business_owner,
                "it_owner": it_owner,
               
