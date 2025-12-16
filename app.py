import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="IT Application Survey – Vietnam Airlines",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_DIR = "data/json"
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# MODERN UI – ENHANCED BRAND STYLE
# =========================
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #F4F7FB 0%, #FFFFFF 100%);
    }
    
    /* Header Styles */
    h1 {
        color: #005EB8;
        font-weight: 700;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }
    
    h2, h3 {
        color: #002B5C;
        font-weight: 600;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 8px;
        color: #002B5C;
        font-weight: 600;
        padding: 0 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FFF8E1;
        color: #005EB8;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFC72C 0%, #FFB000 100%);
        color: #002B5C !important;
        box-shadow: 0 4px 12px rgba(255,199,44,0.3);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #FFC72C 0%, #FFB000 100%);
        color: #002B5C;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255,199,44,0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFD966 0%, #FFC72C 100%);
        box-shadow: 0 6px 20px rgba(255,199,44,0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #005EB8 0%, #003D82 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,94,184,0.3);
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #0073E6 0%, #005EB8 100%);
        box-shadow: 0 6px 20px rgba(0,94,184,0.4);
        transform: translateY(-2px);
    }
    
    /* Card Styles */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0,94,184,0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 12px 32px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #E0E7EF;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #FFC72C;
        box-shadow: 0 0 0 3px rgba(255,199,44,0.1);
    }
    
    /* Radio & Multiselect */
    .stRadio > div {
        background: #F8FAFC;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .stMultiSelect > div > div {
        border-radius: 8px;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #FFC72C 0%, #FFB000 100%);
    }
    
    /* Caption */
    .caption {
        color: #64748B;
        font-size: 0.95rem;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #E0E7EF, transparent);
    }
    
    /* Success Message */
    .stSuccess {
        background-color: #D4EDDA;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28A745;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #005EB8;
        margin-bottom: 1.5rem;
    }
    
    /* Stats Card */
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        text-align: center;
        border-top: 4px solid #FFC72C;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        color: #005EB8;
    }
    
    .stats-label {
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([3, 1])
with col1:
    st.title("✈️ KHẢO SÁT QUY HOẠCH HỆ THỐNG CNTT")
    st.markdown('<p class="caption">Digital IT Landscape Survey | Enterprise Architecture & IT Master Planning</p>', 
                unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">2024</div>
        <div class="stats-label">Vietnam Airlines</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# INFO BOX
# =========================
st.markdown("""
<div class="info-box">
    <strong>📋 Hướng dẫn:</strong> Vui lòng điền đầy đủ thông tin về hệ thống CNTT của đơn vị. 
    Dữ liệu sẽ được sử dụng cho quy hoạch tổng thể kiến trúc doanh nghiệp.
</div>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE INIT
# =========================
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# =========================
# TABS
# =========================
tabs = st.tabs([
    "📋 A. Thông tin chung",
    "🖥️ B. Hạ tầng",
    "💾 C. Dữ liệu",
    "🔗 D. Tích hợp",
    "🔒 E. An toàn",
    "🎯 F. Định hướng",
    "📊 G. Quản lý"
])

# =========================
# TAB A - THÔNG TIN CHUNG
# =========================
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        system_name = st.text_input(
            "Tên hệ thống / phần mềm *",
            placeholder="VD: Passenger Service System",
            help="Tên đầy đủ của hệ thống"
        )
        system_code = st.text_input(
            "Mã hệ thống (System Code) *",
            placeholder="VD: PSS",
            help="Mã viết tắt của hệ thống"
        )
        business_owner = st.text_input(
            "Business Owner *",
            placeholder="Họ tên và chức danh"
        )
        it_owner = st.text_input(
            "IT Owner *",
            placeholder="Họ tên và chức danh"
        )
    
    with col2:
        business_group = st.multiselect(
            "Nhóm nghiệp vụ *",
            ["Khai thác bay", "Thương mại", "Dịch vụ", "Kỹ thuật",
             "Tài chính", "Nhân sự", "An toàn – An ninh", "Quản lý chung"],
            help="Có thể chọn nhiều nhóm"
        )
        vendor = st.text_input(
            "Nhà cung cấp / Đối tác",
            placeholder="VD: Amadeus, SITA"
        )
        system_type = st.multiselect(
            "Loại hệ thống *",
            ["COTS", "SaaS", "In-house", "Outsource", "Legacy"]
        )
        value_chain = st.multiselect(
            "Vai trò chuỗi giá trị",
            ["Core", "Support", "Analytics", "Compliance"]
        )
    
    col3, col4 = st.columns(2)
    with col3:
        deploy_year = st.selectbox(
            "Năm triển khai",
            range(2025, 1999, -1),
            index=0
        )
    
    with col4:
        status = st.radio(
            "Tình trạng hiện tại *",
            ["Đang vận hành", "Nâng cấp", "Thay thế", "Dừng"],
            horizontal=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB B - HẠ TẦNG
# =========================
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        infra_model = st.multiselect(
            "Mô hình hạ tầng *",
            ["On-Premise", "Private Cloud", "Public Cloud", "Hybrid Cloud"],
            help="Có thể chọn nhiều mô hình"
        )
        dc_region = st.text_input(
            "DC / Cloud Region",
            placeholder="VD: Hanoi DC, AWS Singapore"
        )
        infra_provider = st.multiselect(
            "Nhà cung cấp hạ tầng",
            ["AWS", "Azure", "Google Cloud", "Viettel IDC", "VNPT", "FPT", "Nội bộ", "Khác"]
        )
        server_type = st.radio(
            "Loại máy chủ",
            ["Virtual Machine", "Physical Server", "Container", "Serverless"],
            horizontal=True
        )
    
    with col2:
        os_name = st.text_input(
            "Hệ điều hành",
            placeholder="VD: Windows Server 2019, Ubuntu 22.04"
        )
        resource = st.text_input(
            "Tài nguyên (CPU / RAM / Storage)",
            placeholder="VD: 8 vCPU / 32GB RAM / 500GB SSD"
        )
        sla = st.slider(
            "SLA Uptime (%)",
            90, 100, 99,
            help="Service Level Agreement"
        )
        ha_dr = st.multiselect(
            "Giải pháp HA / DR",
            ["Active-Active", "Active-Passive", "Backup Only", "None"]
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB C - DỮ LIỆU
# =========================
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Phân loại dữ liệu")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pii = st.radio(
            "Dữ liệu cá nhân (PII)",
            ["Có", "Không"],
            horizontal=True,
            help="Thông tin định danh cá nhân"
        )
    
    with col2:
        sensitive = st.radio(
            "Dữ liệu nhạy cảm",
            ["Có", "Không"],
            horizontal=True,
            help="Dữ liệu mật, bí mật"
        )
    
    with col3:
        finance = st.radio(
            "Dữ liệu tài chính",
            ["Có", "Không"],
            horizontal=True,
            help="Thông tin thanh toán, giao dịch"
        )
    
    with col4:
        cross_border = st.radio(
            "Dữ liệu xuyên biên giới",
            ["Có", "Không"],
            horizontal=True,
            help="Dữ liệu ra nước ngoài"
        )
    
    st.divider()
    
    col5, col6 = st.columns(2)
    with col5:
        data_source = st.text_input(
            "Source of Truth",
            placeholder="Hệ thống nguồn chính thức",
            help="Hệ thống là nguồn dữ liệu gốc"
        )
        data_volume = st.text_input(
            "Khối lượng dữ liệu",
            placeholder="VD: 10TB, 5M records/day"
        )
    
    with col6:
        data_quality = st.multiselect(
            "Chất lượng dữ liệu",
            ["Đầy đủ", "Chính xác", "Kịp thời", "Nhất quán", "Hợp lệ"]
        )
        data_retention = st.text_input(
            "Thời gian lưu trữ",
            placeholder="VD: 7 năm, Vĩnh viễn"
        )
    
    backup_policy = st.text_area(
        "Chính sách sao lưu",
        placeholder="VD: Daily incremental, Weekly full backup",
        height=80
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB D - TÍCH HỢP
# =========================
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Thông tin tích hợp")
    
    integration_desc = st.text_area(
        "Danh sách hệ thống tích hợp",
        placeholder="Mỗi dòng một hệ thống:\nPSS | Hai chiều | API REST | Real-time\nDCS | Một chiều | SFTP | Batch",
        height=120,
        help="Format: Tên hệ thống | Chiều | Phương thức | Tần suất"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        data_standard = st.multiselect(
            "Chuẩn dữ liệu",
            ["IATA NDC", "AIDX", "EDIFACT", "PADIS", "XML", "JSON", "CSV", "Proprietary"]
        )
        protocol = st.multiselect(
            "Giao thức tích hợp",
            ["REST API", "SOAP", "GraphQL", "gRPC", "Message Queue", "SFTP", "FTP", "WebSocket"]
        )
        message_format = st.multiselect(
            "Định dạng message",
            ["JSON", "XML", "Avro", "Protobuf", "Plain Text"]
        )
    
    with col2:
        api_gateway = st.radio(
            "Sử dụng API Gateway",
            ["Có", "Không"],
            horizontal=True
        )
        esb_usage = st.radio(
            "Sử dụng ESB/Integration Platform",
            ["Có", "Không"],
            horizontal=True
        )
        logging = st.radio(
            "Logging / Monitoring tích hợp",
            ["Có", "Không"],
            horizontal=True
        )
        error_handling = st.text_input(
            "Cơ chế xử lý lỗi",
            placeholder="VD: Retry 3 lần, Dead letter queue"
        )
    
    col3, col4 = st.columns(2)
    with col3:
        integration_frequency = st.selectbox(
            "Tần suất tích hợp",
            ["Real-time", "Near real-time", "Hourly", "Daily", "Weekly", "On-demand"]
        )
    
    with col4:
        peak_tps = st.text_input(
            "Peak TPS (Transaction/second)",
            placeholder="VD: 1000 TPS"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB E - AN TOÀN BẢO MẬT
# =========================
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Bảo mật & Tuân thủ")
    
    col1, col2 = st.columns(2)
    with col1:
        rbac = st.text_input(
            "Mô hình phân quyền (RBAC)",
            placeholder="VD: Admin, Manager, User, Guest"
        )
        auth = st.multiselect(
            "Phương thức xác thực",
            ["SSO (Single Sign-On)", "MFA (Multi-Factor)", "LDAP/AD", 
             "OAuth 2.0", "SAML", "Biometric", "Username/Password"]
        )
        encryption = st.multiselect(
            "Mã hóa",
            ["Data at rest", "Data in transit", "End-to-end", "Database encryption", "Không có"]
        )
        security_scan = st.radio(
            "Quét bảo mật định kỳ",
            ["Có", "Không"],
            horizontal=True
        )
    
    with col2:
        legal = st.multiselect(
            "Tuân thủ pháp lý",
            ["GDPR", "Luật ATTT Việt Nam", "Nghị định 85/2016", 
             "ICAO Annex 17", "PCI-DSS", "ISO 27001", "SOC 2"]
        )
        audit_log = st.radio(
            "Audit Log / Trail",
            ["Có", "Không"],
            horizontal=True,
            help="Ghi nhận lịch sử thao tác"
        )
        penetration_test = st.text_input(
            "Kiểm thử xâm nhập (Pentest)",
            placeholder="VD: Hàng năm, Chưa thực hiện"
        )
        incident_response = st.text_area(
            "Quy trình ứng phó sự cố",
            placeholder="Mô tả quy trình xử lý sự cố bảo mật",
            height=80
        )
    
    col3, col4 = st.columns(2)
    with col3:
        vulnerability_mgmt = st.radio(
            "Quản lý lỗ hổng bảo mật",
            ["Có", "Không"],
            horizontal=True
        )
    
    with col4:
        security_training = st.radio(
            "Đào tạo ATTT cho user",
            ["Có", "Không"],
            horizontal=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB F - ĐỊNH HƯỚNG
# =========================
with tabs[5]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Đánh giá & Định hướng")
    
    col1, col2 = st.columns(2)
    with col1:
        strategy_fit = st.slider(
            "Mức độ phù hợp chiến lược số (1-5)",
            1, 5, 3,
            help="1: Không phù hợp, 5: Rất phù hợp"
        )
        
        business_value = st.slider(
            "Giá trị kinh doanh (1-5)",
            1, 5, 3,
            help="Đóng góp vào mục tiêu kinh doanh"
        )
        
        technical_debt = st.slider(
            "Nợ kỹ thuật (1-5)",
            1, 5, 3,
            help="1: Thấp, 5: Cao"
        )
    
    with col2:
        proposal = st.radio(
            "Đề xuất quy hoạch *",
            ["Giữ nguyên (Retain)", "Nâng cấp (Upgrade)", 
             "Hợp nhất (Consolidate)", "Thay thế (Replace)", 
             "Loại bỏ (Retire)"],
            help="Lựa chọn phương án phù hợp"
        )
        
        priority = st.radio(
            "Độ ưu tiên thực hiện *",
            ["High (Cao)", "Medium (Trung bình)", "Low (Thấp)"],
            horizontal=True
        )
        
        timeline = st.text_input(
            "Thời gian dự kiến",
            placeholder="VD: Q2/2024, 2025-2026"
        )
    
    col3, col4 = st.columns(2)
    with col3:
        estimated_cost = st.text_input(
            "Ước tính chi phí",
            placeholder="VD: 5 tỷ VNĐ, $500K"
        )
    
    with col4:
        roi_expectation = st.text_input(
            "Kỳ vọng ROI",
            placeholder="VD: 2 năm, 150%"
        )
    
    roadmap = st.text_area(
        "Lộ trình chi tiết",
        placeholder="Mô tả các bước thực hiện theo thời gian",
        height=100
    )
    
    risk_assessment = st.text_area(
        "Đánh giá rủi ro",
        placeholder="Các rủi ro tiềm ẩn và biện pháp giảm thiểu",
        height=100
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB G - QUẢN LÝ
# =========================
with tabs[6]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Thông tin quản lý")
    
    col1, col2 = st.columns(2)
    with col1:
        updated_by = st.text_input(
            "Người cập nhật *",
            placeholder="Họ tên và email"
        )
        department = st.text_input(
            "Đơn vị / Phòng ban",
            placeholder="VD: Trung tâm CNTT"
        )
        contact_email = st.text_input(
            "Email liên hệ",
            placeholder="example@vietnamairlines.com"
        )
    
    with col2:
        version = st.text_input(
            "Phiên bản form",
            value="v1.0"
        )
        review_date = st.date_input(
            "Ngày xem xét lại",
            help="Ngày cần cập nhật thông tin"
        )
        approval_status = st.selectbox(
            "Trạng thái phê duyệt",
            ["Draft", "Pending Review", "Approved", "Rejected"]
        )
    
    note = st.text_area(
        "Ghi chú / Nhận xét",
        placeholder="Thông tin bổ sung, lưu ý đặc biệt...",
        height=120
    )
    
    attachments = st.file_uploader(
        "Tài liệu đính kèm",
        accept_multiple_files=True,
        help="Kiến trúc, sơ đồ, tài liệu kỹ thuật..."
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DATA COLLECTION
# =========================
form_data = {
    # Tab A
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
    
    # Tab B
    "infra_model": infra_model,
    "dc_region": dc_region,
    "infra_provider": infra_provider,
    "server_type": server_type,
    "os_name": os_name,
    "resource": resource,
    "sla": sla,
    "ha_dr": ha_dr,
    
    # Tab C
    "pii": pii,
    "sensitive": sensitive,
    "finance": finance,
    "cross_border": cross_border,
    "data_source": data_source,
    "data_volume": data_volume,
    "data_quality": data_quality,
    "data_retention": data_retention,
    "backup_policy": backup_policy,
    
    # Tab D
    "integration": integration_desc,
    "data_standard": data_standard,
    "protocol": protocol,
    "message_format": message_format,
    "api_gateway": api_gateway,
    "esb_usage": esb_usage,
    "logging": logging,
    "error_handling": error_handling,
    "integration_frequency": integration_frequency,
    "peak_tps": peak_tps,
    
    # Tab E
    "rbac": rbac,
    "auth": auth,
    "encryption": encryption,
    "security_scan": security_scan,
    "legal": legal,
    "audit_log": audit_log,
    "penetration_test": penetration_test,
    "incident_response": incident_response,
    "vulnerability_mgmt": vulnerability_mgmt,
    "security_training": security_training,
    
     # Tab F
    "strategy_fit": strategy_fit,
    "business_value": business_value,
    "technical_debt": technical_debt,
    "proposal": proposal,
    "priority": priority,
    "timeline": timeline,
    "estimated_cost": estimated_cost,
    "roi_expectation": roi_expectation,
    "roadmap": roadmap,
    "risk_assessment": risk_assessment,
    
    # Tab G
    "updated_by": updated_by,
    "department": department,
    "contact_email": contact_email,
    "updated_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "version": version,
    "review_date": str(review_date) if 'review_date' in locals() else "",
    "approval_status": approval_status,
    "note": note
}

# =========================
# ENHANCED PDF EXPORT
# =========================
def export_pdf(data: dict):
    """Tạo PDF báo cáo chuyên nghiệp với định dạng đẹp"""
    buffer = BytesIO()
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleCenter",
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor('#005EB8'),
        spaceAfter=20,
        fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#002B5C'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=2,
        borderColor=colors.HexColor('#FFC72C'),
        borderPadding=5,
        backColor=colors.HexColor('#FFF8E1')
    ))
    styles.add(ParagraphStyle(
        name="SubHeader",
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        alignment=TA_CENTER,
        spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name="BodyText",
        fontSize=10,
        leading=14
    ))
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        topMargin=50,
        bottomMargin=50,
        leftMargin=50,
        rightMargin=50
    )
    elements = []
    
    # Table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#002B5C')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E7EF')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])
    
    def create_section(title, items):
        """Tạo section với table"""
        elements.append(Paragraph(title, styles["SectionHeader"]))
        elements.append(Spacer(1, 10))
        
        table_data = []
        for key, value in items:
            # Format value
            if isinstance(value, list):
                value = ", ".join(value) if value else "N/A"
            elif not value:
                value = "N/A"
            
            table_data.append([
                Paragraph(f"<b>{key}</b>", styles["BodyText"]),
                Paragraph(str(value), styles["BodyText"])
            ])
        
        table = Table(table_data, colWidths=[180, 320])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Header
    elements.append(Paragraph(
        "BÁO CÁO KHẢO SÁT HỆ THỐNG CNTT",
        styles["TitleCenter"]
    ))
    elements.append(Paragraph(
        "VIETNAM AIRLINES | IT LANDSCAPE SURVEY",
        styles["SubHeader"]
    ))
    elements.append(Spacer(1, 10))
    
    # Metadata box
    meta_data = [
        ["Ngày tạo báo cáo:", data.get("updated_date", "")],
        ["Người cập nhật:", data.get("updated_by", "")],
        ["Phiên bản:", data.get("version", "")]
    ]
    meta_table = Table(meta_data, colWidths=[150, 350])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#005EB8')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#005EB8')),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 20))
    
    # Section A - Thông tin chung
    create_section("A. THÔNG TIN CHUNG", [
        ("Tên hệ thống", data.get("system_name", "")),
        ("Mã hệ thống", data.get("system_code", "")),
        ("Nhóm nghiệp vụ", data.get("business_group", [])),
        ("Business Owner", data.get("business_owner", "")),
        ("IT Owner", data.get("it_owner", "")),
        ("Nhà cung cấp", data.get("vendor", "")),
        ("Loại hệ thống", data.get("system_type", [])),
        ("Vai trò chuỗi giá trị", data.get("value_chain", [])),
        ("Năm triển khai", data.get("deploy_year", "")),
        ("Tình trạng", data.get("status", ""))
    ])
    
    elements.append(PageBreak())
    
    # Section B - Hạ tầng
    create_section("B. HẠ TẦNG", [
        ("Mô hình hạ tầng", data.get("infra_model", [])),
        ("DC / Cloud Region", data.get("dc_region", "")),
        ("Nhà cung cấp hạ tầng", data.get("infra_provider", [])),
        ("Loại máy chủ", data.get("server_type", "")),
        ("Hệ điều hành", data.get("os_name", "")),
        ("Tài nguyên", data.get("resource", "")),
        ("SLA Uptime", f"{data.get('sla', '')}%"),
        ("HA / DR", data.get("ha_dr", []))
    ])
    
    # Section C - Dữ liệu
    create_section("C. DỮ LIỆU", [
        ("Dữ liệu cá nhân (PII)", data.get("pii", "")),
        ("Dữ liệu nhạy cảm", data.get("sensitive", "")),
        ("Dữ liệu tài chính", data.get("finance", "")),
        ("Dữ liệu xuyên biên giới", data.get("cross_border", "")),
        ("Source of Truth", data.get("data_source", "")),
        ("Khối lượng dữ liệu", data.get("data_volume", "")),
        ("Chất lượng dữ liệu", data.get("data_quality", [])),
        ("Thời gian lưu trữ", data.get("data_retention", "")),
        ("Chính sách sao lưu", data.get("backup_policy", ""))
    ])
    
    elements.append(PageBreak())
    
    # Section D - Tích hợp
    create_section("D. TÍCH HỢP", [
        ("Danh sách tích hợp", data.get("integration", "")),
        ("Chuẩn dữ liệu", data.get("data_standard", [])),
        ("Giao thức", data.get("protocol", [])),
        ("Định dạng message", data.get("message_format", [])),
        ("API Gateway", data.get("api_gateway", "")),
        ("ESB/Integration Platform", data.get("esb_usage", "")),
        ("Logging/Monitoring", data.get("logging", "")),
        ("Xử lý lỗi", data.get("error_handling", "")),
        ("Tần suất tích hợp", data.get("integration_frequency", "")),
        ("Peak TPS", data.get("peak_tps", ""))
    ])
    
    # Section E - An toàn bảo mật
    create_section("E. AN TOÀN BẢO MẬT", [
        ("Mô hình phân quyền", data.get("rbac", "")),
        ("Xác thực", data.get("auth", [])),
        ("Mã hóa", data.get("encryption", [])),
        ("Quét bảo mật", data.get("security_scan", "")),
        ("Tuân thủ pháp lý", data.get("legal", [])),
        ("Audit Log", data.get("audit_log", "")),
        ("Penetration Test", data.get("penetration_test", "")),
        ("Ứng phó sự cố", data.get("incident_response", "")),
        ("Quản lý lỗ hổng", data.get("vulnerability_mgmt", "")),
        ("Đào tạo ATTT", data.get("security_training", ""))
    ])
    
    elements.append(PageBreak())
    
    # Section F - Định hướng
    create_section("F. ĐỊNH HƯỚNG", [
        ("Phù hợp chiến lược số", f"{data.get('strategy_fit', '')}/5"),
        ("Giá trị kinh doanh", f"{data.get('business_value', '')}/5"),
        ("Nợ kỹ thuật", f"{data.get('technical_debt', '')}/5"),
        ("Đề xuất quy hoạch", data.get("proposal", "")),
        ("Độ ưu tiên", data.get("priority", "")),
        ("Thời gian dự kiến", data.get("timeline", "")),
        ("Ước tính chi phí", data.get("estimated_cost", "")),
        ("Kỳ vọng ROI", data.get("roi_expectation", "")),
        ("Lộ trình", data.get("roadmap", "")),
        ("Đánh giá rủi ro", data.get("risk_assessment", ""))
    ])
    
    # Section G - Quản lý
    create_section("G. QUẢN LÝ", [
        ("Người cập nhật", data.get("updated_by", "")),
        ("Đơn vị/Phòng ban", data.get("department", "")),
        ("Email liên hệ", data.get("contact_email", "")),
        ("Ngày cập nhật", data.get("updated_date", "")),
        ("Phiên bản", data.get("version", "")),
        ("Ngày xem xét lại", data.get("review_date", "")),
        ("Trạng thái phê duyệt", data.get("approval_status", "")),
        ("Ghi chú", data.get("note", ""))
    ])
    
    # Footer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(
        "_______________________________________________",
        styles["TitleCenter"]
    ))
    elements.append(Paragraph(
        "© Vietnam Airlines - IT Department | Confidential",
        styles["SubHeader"]
    ))
    
    # Build PDF
    doc.build(elements)
    return buffer.getvalue()

# =========================
# VALIDATION
# =========================
def validate_form():
    """Kiểm tra các trường bắt buộc"""
    errors = []
    
    if not system_name:
        errors.append("Tên hệ thống")
    if not system_code:
        errors.append("Mã hệ thống")
    if not business_group:
        errors.append("Nhóm nghiệp vụ")
    if not business_owner:
        errors.append("Business Owner")
    if not it_owner:
        errors.append("IT Owner")
    if not updated_by:
        errors.append("Người cập nhật")
    
    return errors

# =========================
# ACTIONS SECTION
# =========================
st.divider()

# Summary stats
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown("""
    <div class="stats-card">
        <div class="stats-number">✓</div>
        <div class="stats-label">Form Completion</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    completed = sum([1 for v in form_data.values() if v])
    total = len(form_data)
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{completed}/{total}</div>
        <div class="stats-label">Fields Filled</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{data.get('sla', 99)}%</div>
        <div class="stats-label">SLA Target</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    priority_color = {"High (Cao)": "🔴", "Medium (Trung bình)": "🟡", "Low (Thấp)": "🟢"}
    priority_icon = priority_color.get(priority, "⚪")
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{priority_icon}</div>
        <div class="stats-label">Priority</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    if st.button("💾 LƯU
