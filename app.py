import streamlit as st
import json, os
from datetime import datetime

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Vietnam Airlines | Khảo sát CNTT",
    layout="wide"
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

if "form" not in st.session_state:
    st.session_state.form = {}

f = st.session_state.form

# ======================
# BRAND STYLE – VIETNAM AIRLINES
# ======================
st.markdown("""
<style>
body {
    background-color: #F7F9FC;
}
header {visibility: hidden;}
.block-container {
    padding-top: 1.5rem;
}
.vna-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 22px;
    border: 1px solid #E5EAF1;
    margin-bottom: 24px;
}
.vna-title {
    color: #005EB8;
    font-weight: 700;
}
.vna-sub {
    color: #4B5563;
}
.stTabs [role="tab"] {
    padding: 12px 18px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background-color: #005EB8;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown(
    "<h2 class='vna-title'>✈️ VIETNAM AIRLINES</h2>"
    "<h4 class='vna-sub'>Khảo sát Quy hoạch Hệ thống CNTT toàn Tổng Công ty</h4>",
    unsafe_allow_html=True
)

st.divider()

# ======================
# TABS A – G
# ======================
tabA, tabB, tabC, tabD, tabE, tabF, tabG = st.tabs([
    "A. Thông tin chung",
    "B. Hạ tầng",
    "C. Dữ liệu",
    "D. Tích hợp",
    "E. An toàn & Tuân thủ",
    "F. Đánh giá & Định hướng",
    "G. Lưu & Quản lý"
])

# ======================
# TAB A
# ======================
with tabA:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("A. Thông tin tổng quan")

    f["system_name"] = st.text_input("Tên hệ thống", f.get("system_name",""))
    f["system_code"] = st.text_input("Mã hệ thống", f.get("system_code",""))
    f["business_owner"] = st.text_input("Đơn vị nghiệp vụ sở hữu", f.get("business_owner",""))
    f["it_owner"] = st.text_input("Đơn vị CNTT quản lý", f.get("it_owner",""))

    f["system_type"] = st.multiselect(
        "Loại hệ thống",
        ["COTS", "SaaS", "In-house", "Outsource", "Legacy"],
        f.get("system_type", [])
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB B
# ======================
with tabB:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("B. Hạ tầng & Triển khai")

    f["infra_model"] = st.multiselect(
        "Mô hình hạ tầng",
        ["On-Prem", "Private Cloud", "Public Cloud", "Hybrid"],
        f.get("infra_model", [])
    )

    f["infra_provider"] = st.multiselect(
        "Nhà cung cấp",
        ["AWS", "Azure", "Viettel", "VNPT", "FPT", "Khác"],
        f.get("infra_provider", [])
    )

    f["sla"] = st.slider("Mức SLA (%)", 90, 100, f.get("sla", 99))
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB C
# ======================
with tabC:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("C. Dữ liệu & Khai thác")

    f["pii"] = st.radio("Dữ liệu cá nhân (PII)", ["Có", "Không"], horizontal=True)
    f["sensitive"] = st.radio("Dữ liệu nhạy cảm", ["Có", "Không"], horizontal=True)
    f["bi_ai"] = st.radio("Cung cấp cho BI / AI", ["Có", "Không"], horizontal=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB D
# ======================
with tabD:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("D. Tích hợp & Chia sẻ")

    f["integration"] = st.text_area(
        "Danh sách hệ thống tích hợp",
        f.get("integration",""),
        placeholder="VD: PSS – API – Hai chiều"
    )

    f["api_gateway"] = st.radio("Thông qua API Gateway", ["Có", "Không"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB E
# ======================
with tabE:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("E. An toàn thông tin & Tuân thủ")

    f["auth"] = st.multiselect(
        "Cơ chế xác thực",
        ["SSO", "MFA", "RBAC", "Khác"],
        f.get("auth", [])
    )

    f["legal"] = st.multiselect(
        "Tuân thủ",
        ["Luật ATTT VN", "GDPR", "ICAO", "ISO 27001"],
        f.get("legal", [])
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB F
# ======================
with tabF:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("F. Đánh giá & Định hướng")

    f["strategy_fit"] = st.slider("Mức độ phù hợp chiến lược số", 1, 5, f.get("strategy_fit",3))
    f["proposal"] = st.radio(
        "Định hướng xử lý",
        ["Giữ nguyên", "Nâng cấp", "Hợp nhất", "Thay thế"],
        horizontal=True
    )
    f["priority"] = st.radio(
        "Mức ưu tiên",
        ["High", "Medium", "Low"],
        horizontal=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ======================
# TAB G – SAVE
# ======================
with tabG:
    st.markdown("<div class='vna-card'>", unsafe_allow_html=True)
    st.subheader("G. Lưu & Quản lý dữ liệu")

    f["updated_by"] = st.text_input("Người cập nhật", f.get("updated_by",""))
    f["updated_date"] = datetime.now().strftime("%d/%m/%Y")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 LƯU TẠM"):
            filename = f"DRAFT_{f['business_owner']}_{f['system_code']}.json".replace(" ","_")
            with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as fp:
                json.dump(f, fp, ensure_ascii=False, indent=2)
            st.success(f"Đã lưu tạm: {filename}")

    with col2:
        if st.button("✅ HOÀN TẤT & LƯU"):
            filename = f"{f['business_owner']}_{f['system_code']}.json".replace(" ","_")
            with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as fp:
                json.dump(f, fp, ensure_ascii=False, indent=2)
            st.success(f"Đã lưu chính thức: {filename}")

    st.markdown("</div>", unsafe_allow_html=True)
