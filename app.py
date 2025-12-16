import streamlit as st
import json, os
from datetime import datetime

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Vietnam Airlines | IT Survey",
    layout="wide"
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "form" not in st.session_state:
    st.session_state.form = {
        "A": {"A1": {}, "A2": {}, "A3": {}},
        "B": {"B1": {}, "B2": {}, "B3": {}},
        "C": {"C1": {}, "C2": {}, "C3": {}},
        "D": {"D1": {}, "D2": {}, "D3": {}},
        "E": {},
        "F": {},
        "G": {}
    }

f = st.session_state.form

# ======================
# DARK MODE – VNA BRAND
# ======================
st.markdown("""
<style>
html, body {
    background-color: #0B1220;
    color: #E5E7EB;
    font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
header {visibility: hidden;}
.block-container {
    padding: 1.4rem 2rem;
}

/* ===== HEADER ===== */
.vna-header {
    background: linear-gradient(90deg,#005EB8,#003A75);
    padding: 24px 28px;
    border-radius: 18px;
    margin-bottom: 28px;
}
.vna-header h2 {
    margin: 0;
    color: white;
}
.vna-header p {
    margin: 6px 0 0;
    color: #E5E7EB;
    opacity: 0.9;
}

/* ===== CARDS ===== */
.vna-card {
    background: #111A2E;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #1F2A44;
    margin-bottom: 26px;
}
.vna-card:hover {
    border-color: #005EB8;
}

/* ===== INPUTS ===== */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select {
    background-color: #0B1220 !important;
    color: #E5E7EB !important;
    border-radius: 10px !important;
    border: 1px solid #1F2A44 !important;
    padding: 10px 12px !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #005EB8 !important;
    box-shadow: 0 0 0 2px rgba(0,94,184,0.25);
}

/* ===== LABELS ===== */
label {
    color: #E5E7EB !important;
}

/* ===== RADIO / CHECKBOX ===== */
.stRadio label,
.stCheckbox label {
    font-size: 0.95rem;
}

/* ===== SLIDER ===== */
.stSlider > div {
    color: #F5C400;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background-color: #005EB8;
    color: white;
    border-radius: 12px;
    padding: 10px 24px;
    border: none;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #004A94;
}
.stButton.secondary > button {
    background-color: #F5C400;
    color: #0B1220;
}

/* ===== TABS ===== */
.stTabs [role="tab"] {
    padding: 14px 20px;
    font-weight: 600;
    border-radius: 14px;
    background: #111A2E;
    margin-right: 8px;
    color: #9CA3AF;
}
.stTabs [aria-selected="true"] {
    background-color: #005EB8;
    color: white;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
    .block-container {
        padding: 1rem;
    }
    .vna-card {
        padding: 18px;
    }
    .stTabs [role="tab"] {
        padding: 10px 14px;
        font-size: 0.9rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown("""
<div class="vna-header">
    <h2>✈️ VIETNAM AIRLINES</h2>
    <p>Khảo sát Quy hoạch Hệ thống CNTT & Kiến trúc Doanh nghiệp</p>
</div>
""", unsafe_allow_html=True)

# ======================
# TABS
# ======================
tabA, tabB, tabC, tabD, tabE, tabF, tabG = st.tabs([
    "A. Thông tin chung",
    "B. Hạ tầng",
    "C. Dữ liệu",
    "D. Tích hợp",
    "E. An toàn – Tuân thủ",
    "F. Đánh giá – Quy hoạch",
    "G. Lưu & Quản lý"
])

# ======================
# TAB A
# ======================
with tabA:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("A1. Thông tin định danh")

    col1, col2 = st.columns(2)
    with col1:
        f["A"]["A1"]["system_name"] = st.text_input("Tên hệ thống")
        f["A"]["A1"]["system_code"] = st.text_input("Mã hệ thống")
        f["A"]["A1"]["business_owner"] = st.text_input("Đơn vị nghiệp vụ")

    with col2:
        f["A"]["A1"]["it_owner"] = st.text_input("Đơn vị CNTT")
        f["A"]["A1"]["vendor"] = st.text_input("Nhà cung cấp")
        f["A"]["A1"]["system_type"] = st.multiselect(
            "Loại hệ thống",
            ["COTS","SaaS","In-house","Outsource","Legacy"]
        )

    f["A"]["A1"]["business_group"] = st.multiselect(
        "Nhóm nghiệp vụ",
        ["Khai thác bay","Thương mại","Dịch vụ","Kỹ thuật","Tài chính","Nhân sự","An toàn – An ninh","Quản lý chung"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB B
# ======================
with tabB:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["B"]["B1"]["infra_model"] = st.multiselect(
        "Mô hình hạ tầng",
        ["On-Prem","Private Cloud","Public Cloud","Hybrid"]
    )
    f["B"]["B1"]["provider"] = st.multiselect(
        "Nhà cung cấp",
        ["AWS","Azure","Viettel","VNPT","FPT","Khác"]
    )
    f["B"]["B3"]["sla"] = st.slider("SLA (%)",90,100)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB C
# ======================
with tabC:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["C"]["C1"]["pii"] = st.radio("Dữ liệu cá nhân (PII)",["Có","Không"],horizontal=True)
    f["C"]["C1"]["sensitive"] = st.radio("Dữ liệu nhạy cảm",["Có","Không"],horizontal=True)
    f["C"]["C3"]["bi_ai"] = st.radio("Cung cấp cho BI/AI",["Có","Không"],horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB D
# ======================
with tabD:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["D"]["D1"]["systems"] = st.text_area(
        "Danh sách hệ thống tích hợp",
        placeholder="PSS | Hai chiều | API"
    )
    f["D"]["D3"]["api_gateway"] = st.radio("API Gateway",["Có","Không"],horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB E
# ======================
with tabE:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["E"]["auth"] = st.multiselect("Xác thực",["SSO","MFA","Khác"])
    f["E"]["legal"] = st.multiselect(
        "Tuân thủ pháp lý",
        ["Luật ATTT VN","GDPR","ICAO Annex 17","Quy chế ANTT TCTHK"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB F
# ======================
with tabF:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["F"]["strategy_fit"] = st.slider("Phù hợp chiến lược số",1,5)
    f["F"]["proposal"] = st.radio(
        "Định hướng",
        ["Giữ nguyên","Nâng cấp","Hợp nhất","Thay thế"],
        horizontal=True
    )
    f["F"]["priority"] = st.radio(
        "Ưu tiên",
        ["High","Medium","Low"],
        horizontal=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB G – SAVE
# ======================
with tabG:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    f["G"]["updated_by"] = st.text_input("Người cập nhật")
    f["G"]["updated_date"] = datetime.now().strftime("%d/%m/%Y")
    f["G"]["version"] = st.text_input("Phiên bản","v1.0")
    f["G"]["note"] = st.text_area("Ghi chú")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 LƯU TẠM"):
            fn = f"DRAFT_{f['A']['A1'].get('system_code','NA')}.json"
            with open(os.path.join(DATA_DIR,fn),"w",encoding="utf-8") as fp:
                json.dump(f,fp,ensure_ascii=False,indent=2)
            st.success(f"Đã lưu tạm: {fn}")

    with col2:
        if st.button("✅ HOÀN TẤT"):
            fn = f"{f['A']['A1'].get('system_code','NA')}.json"
            with open(os.path.join(DATA_DIR,fn),"w",encoding="utf-8") as fp:
                json.dump(f,fp,ensure_ascii=False,indent=2)
            st.success(f"Đã lưu chính thức: {fn}")

    st.markdown("</div>", unsafe_allow_html=True)
